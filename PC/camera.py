import cv2
import numpy as np
import matplotlib.pyplot as plt

from object_detection import ObjectDetection

objDetect = ObjectDetection()

class Camera:
    def __init__(self):
        pass
                
    def __del__(self):
        pass
    
    def preprocess(self):
        width = 640
        height = 480
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # N,C,H,W = batch size, number of channels, height, width.
        H, W = 736, 992

        while cv2.waitKey(33) < 0:
            _, frame = capture.read()
            
            resized_image = cv2.resize(frame, (W, H))

            # Reshape to the network input shape.
            input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

            # Call the convert_result_to_image function after obtaining inference results.
            # plt.figure(figsize=(10, 6))
            # plt.axis("off")

            cv2.imshow("VideoFrame", objDetect.obj_detect(frame, resized_image, input_image, conf_labels=True))
            #plt.show()
            