import socket
import struct
import cv2
import numpy as np
from PyQt5.QtCore import QThread

# 서버 설정
host = "127.0.0.1"
port = 5000

class ReceiveFrame(QThread):    
    def __init__(self, frame_queue):
        super().__init__()        
        self.frame_queue = frame_queue
        
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"서버 대기 중... {self.host}:{self.port}")
        
    def __del__(self):
        self.server_socket.close()
        print("서버를 닫습니다..")
        
    def run(self):
        # 클라이언트 연결 대기
        client_socket, addr = self.server_socket.accept()
        print(f"클라이언트 연결됨: {addr}")
        
        while True:
            frame_len = struct.unpack("!I", client_socket.recv(4))[0]
            frame_data = b""
            
            while len(frame_data) < frame_len:
                chunk = client_socket.recv(min(frame_len - len(frame_data), 4096))
                if not chunk:
                    break
                frame_data += chunk
                
            frame_np = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), 1)
            self.frame_queue.put(frame_np)

