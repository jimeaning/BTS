import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
import openvino as ov

object_list = ["Human", "Car", "Plane"]

# For each detection, the description is in the [x_min, y_min, x_max, y_max, conf] format:
# The image passed here is in BGR format with changed width and height. To display it in colors expected by matplotlib, use cvtColor function
def convert_result_to_image(bgr_image, resized_image, boxes, label, threshold=0.3, conf_labels=True):
    global object_list
    
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
        label_index = label_index + 1        

    return rgb_image

def thread_cam(q):
    """
    영상을 1장 캡쳐해서 큐에 저장
    """
    # sleep(0.2)
    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    while True:
        _, frame = cam.read()
        
        if frame is None:
            break
        
        q.put(("Cam", frame))
        sleep(1/30)


def thread_detection(q1, q2):
    """
    큐에 저장된 프레임을 inferencing해서 출력
    """
    model_xml_path = "./otx_v1/otx-workspace-DETECTION/outputs/export/openvino.xml"
   
    core = ov.Core()

    model = core.read_model(model=model_xml_path)

    compiled_model = core.compile_model(model=model, device_name="CPU")

    input_layer_ir = compiled_model.input(0)
    output_layer_ir = compiled_model.output("boxes")
    label_layer_ir = compiled_model.output("labels")
    H, W = 736, 992
    
    while True:
        try:
            (name, data) = q1.get_nowait()
        except Empty:
            continue
        resized_image = cv2.resize(data, (W, H))
        input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)
        boxes = compiled_model([input_image])[output_layer_ir]
        boxes = boxes[0]
        labels = compiled_model([input_image])[label_layer_ir]
        label = labels[0]
        q2.put(("Detect", convert_result_to_image(data, resized_image, boxes, label, conf_labels=True)))
        q1.task_done()
    
def main():
    """
    큐에 저장된 정보를 바탕으로 메인 스레드 동작 실행
    """   
    q = Queue()
    d_q = Queue()
    
    thread1 = threading.Thread(target=thread_cam, args=(q,))
    thread2 = threading.Thread(target=thread_detection, args=(q,d_q,))
    
    thread1.start()
    
    thread2.start()
    
    while True:
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
        
        try:
            (name, data) = d_q.get_nowait()
        except Empty:
            continue
        
        if name == 'Detect':
            cv2.imshow(name, data)
            
        #q.task_done()
        d_q.task_done()

    thread2.join()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
