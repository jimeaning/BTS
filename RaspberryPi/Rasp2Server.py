import socket
import cv2
import struct

# 서버 설정
host = "10.10.15.103"
port = 5000

class SendFrame:
    def __init__(self):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def __del__(self):
        self.client_socket.close()

    def send_frame(self, frame):
        _, img_encode = cv2.imencode('.jpg', frame)
        img_bytes = img_encode.tobytes()
        
        self.client_socket.sendall(struct.pack("!I", len(img_bytes)))
        
        self.client_socket.sendall(img_bytes)

width = 640
height = 480
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

sendframe = SendFrame()


while True:
    _, frame = capture.read()
    sendframe.send_frame(frame)
    
