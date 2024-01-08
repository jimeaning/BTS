import cv2
import matplotlib.pyplot as plt
import numpy as np
import openvino as ov

from time import sleep

image_folder = "900/Human/"
save_number = 1

def convert_result_to_image(bgr_image, resized_image, boxes, label, threshold=0.3, conf_labels=True):
    '''
    detection된 ROI를 토대로 이미지 crop
    '''
    global save_number, image_folder
    
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
        if label[label_index] == 0: # 0 : Human | 1 : Car | 2 : Plane
            if conf > threshold:
                # Convert float to int and multiply corner position of each box by x and y ratio.
                # If the bounding box is found at the top of the image, 
                # position the upper box bar little lower to make it visible on the image. 
                (x_min, y_min, x_max, y_max) = [
                    int(max(corner_position * ratio_y, 10)) if idx % 2 
                    else int(corner_position * ratio_x)
                    for idx, corner_position in enumerate(box[:-1])
                ]
            
                crop_image = rgb_image[y_min:y_max, x_min:x_max]
                crop_image = cv2.cvtColor(crop_image, cv2.COLOR_RGB2BGR)
                save_name = "human_crop/human{0:04d}.jpeg".format(save_number)
                save_full_name = "./"+image_folder+save_name
                print(save_number)
                cv2.imwrite(save_full_name,crop_image)
                save_number = save_number + 1
                # Write crop image
        label_index = label_index + 1
            

model_xml_path = "./otx_v1/otx-workspace-DETECTION/outputs/export/openvino.xml"
   
core = ov.Core()
model = core.read_model(model=model_xml_path)
compiled_model = core.compile_model(model=model, device_name="CPU")

input_layer_ir = compiled_model.input(0)
output_layer_ir = compiled_model.output("boxes")
label_layer_ir = compiled_model.output("labels")
# print(model)

image_number = 1

while True:
    image_name = "human{0:04d}.jpeg".format(image_number)

    image_full_name = "./"+image_folder+image_name
    
    print("*** ",image_full_name)
    # Text detection models expect an image in BGR format.
    image = cv2.imread(str(image_full_name))

    # N,C,H,W = batch size, number of channels, height, width.
    H, W = 736, 992

    # sleep(0.03)
    # Resize the image to meet network expected input sizes.
    resized_image = cv2.resize(image, (W, H))

    # Reshape to the network input shape.
    input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

    # Create an inference request.

    boxes = compiled_model([input_image])[output_layer_ir]
    boxes = boxes[0]

    labels = compiled_model([input_image])[label_layer_ir]
    label = labels[0]
    # Call the convert_result_to_image function after obtaining inference results.
    convert_result_to_image(image, resized_image, boxes, label, conf_labels=True)
    image_number = image_number + 1