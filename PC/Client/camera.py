import cv2
import numpy as np
import matplotlib.pyplot as plt
import queue
import socket
import struct

from object_detection import ObjectDetection
from send_frame import SendFrame

objDetect = ObjectDetection()
sendFrame = SendFrame()

class Camera:
    def __init__(self):
        self.host = "10.10.15.103"
        self.port = 5000
        self.frame_queue = queue.Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"서버 대기 중... {self.host}:{self.port}")
                
    def __del__(self):
        self.server_socket.close()
        print("서버를 닫습니다..")
    
    def preprocess(self):
        client_socket, addr = self.server_socket.accept()
        print(f"클라이언트 연결됨: {addr}")
        
        # N,C,H,W = batch size, number of channels, height, width.
        H, W = 736, 992

        while True:
            frame_len = struct.unpack("!I", client_socket.recv(4))[0]
            frame_data = b""
            
            while len(frame_data) < frame_len:
                chunk = client_socket.recv(min(frame_len - len(frame_data), 4096))
                if not chunk:
                    break
                frame_data += chunk
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), 1)
            resized_image = cv2.resize(frame, (W, H))
            
            # Reshape to the network input shape.
            input_image = np.expand_dims(resized_image.transpose(2, 0, 1), 0)

            # Call the convert_result_to_image function after obtaining inference results.
            # plt.figure(figsize=(10, 6))
            # plt.axis("off")
            
            result = objDetect.obj_detect(frame, resized_image, input_image, conf_labels=True)
            sendFrame.send_frame(result)
            
            # cv2.imshow("VideoFrame", result)
            # cv2.waitKey(10)
            # plt.show()
            