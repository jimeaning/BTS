import cv2
import matplotlib.pyplot as plt
import numpy as np
import openvino as ov
from pathlib import Path

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import socket

# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = "10.10.15.104"
server_port = 3000
server_addr_port = (server_ip, server_port)

def send_message(msg):
    bytes_to_send = str.encode(msg)    
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.sendto(bytes_to_send, server_addr_port)

object_list = ["Human", "Car", "Plane"]

capture = cv2.VideoCapture(0)
WIDTH = 640
HEIGHT = 480
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

send_flag = 0

# For each detection, the description is in the [x_min, y_min, x_max, y_max, conf] format:
# The image passed here is in BGR format with changed width and height. To display it in colors expected by matplotlib, use cvtColor function
def convert_result_to_image(bgr_image, resized_image, boxes, label, threshold=0.5, conf_labels=True):
    global object_list
    global send_flag
    
    # Define colors for boxes and descriptions.
    colors = {"red": (255, 0, 0), "green": (0, 255, 0)}

    # Fetch the image shapes to calculate a ratio.
    (real_y, real_x), (resized_y, resized_x) = bgr_image.shape[:2], resized_image.shape[:2]
    ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

    # Convert the base image from BGR to RGB format.
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    label_index = 0
    # Iterate through non-zero boxes.
    for box in boxes:
        # Pick a confidence factor from the last place in an array.
        conf = box[-1]
        if conf > threshold:
            # Convert float to int and multiply corner position of each box by x and y ratio.
            # If the bounding box is found at the top of the image, 
            # position the upper box bar little lower to make it visible on the image. 
            (x_min, y_min, x_max, y_max) = [
                int(max(corner_position * ratio_y, 10)) if idx % 2 
                else int(corner_position * ratio_x)
                for idx, corner_position in enumerate(box[:-1])
            ]

            # Draw a box based on the position, parameters in rectangle function are: image, start_point, end_point, color, thickness.
            rgb_image = cv2.rectangle(rgb_image, (x_min, y_min), (x_max, y_max), colors["green"], 3)

            # Add text to the image based on position and confidence.
            # Parameters in text function are: image, text, bottom-left_corner_textfield, font, font_scale, color, thickness, line_type.
            if conf_labels:
                rgb_image = cv2.putText(
                    rgb_image,
                    f"{object_list[label[label_index]]}, {conf:.2f}",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    colors["red"],
                    2,
                    cv2.LINE_AA,
                )
            mid = int((x_max - x_min) / 2 + x_min)
            
            if send_flag == 0:
                if mid < 200:
                    send_message("1")
                    print("send classification message")
                    send_flag = 1
                    #print("****",mid)
            elif send_flag == 1:
                if 300 < mid < 340:
                    send_message("9")
                    print("send stop message")
                    send_flag = 0
                    #print(mid)
                    
            
        label_index = label_index + 1

    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    
    
    return rgb_image

# model_xml_path = "./otx_v1/otx-workspace-DETECTION/outputs/export/openvino.xml"
model_xml_path = "./model/detection/v1/openvino.xml"
   
core = ov.Core()

model = core.read_model(model=model_xml_path)

compiled_model = core.compile_model(model=model, device_name="CPU")

input_layer_ir = compiled_model.input(0)
output_layer_ir = compiled_model.output("boxes")
label_layer_ir = compiled_model.output("labels")
# print(label_layer_ir)

# Download the image from the openvino_notebooks storage
# image_filename = "./datum_v1/export-coco/images/test/hellicopter0067.jpeg"

# Text detection models expect an image in BGR format.
# image = cv2.imread(str(image_filename))

# N,C,H,W = batch size, number of channels, height, width.
H, W = 736, 992

while cv2.waitKey(33) < 0:
    # sleep(0.03)
    ret, frame = capture.read()
    # Resize the image to meet network expected input sizes.
    resized_image = cv2.resize(frame, (W, H))

    # Reshape to the network input shape.
    input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Create an inference request.

    boxes = compiled_model([input_image])[output_layer_ir]
    boxes = boxes[0]
    labels = compiled_model([input_image])[label_layer_ir]
    label = labels[0]
    #print(labels)
    #print(boxes)
    # Remove zero only boxes.
    # boxes = boxes[~np.all(boxes == 0, axis=1)]

    # Call the convert_result_to_image function after obtaining inference results.
    plt.figure(figsize=(10, 6))
    plt.axis("off")

    
    
    cv2.imshow("VideoFrame", convert_result_to_image(frame, resized_image, boxes, label, conf_labels=True))
    #plt.show()

