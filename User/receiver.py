"""
콘솔 메시지 통신을 위한 모듈
"""
import socket
from PyQt5.QtCore import QThread, pyqtSignal

server_ip = "10.10.15.103"
server_port = 4000
        

class ReceiveMessage(QThread):
    """콘솔 메시지 통신을 위한 클래스"""
    rcv_msg_signal = pyqtSignal()
    
    def __init__(self, msg_queue):
        super().__init__()        
        self.msg_queue = msg_queue
        
        self.host = server_ip
        self.port = server_port
        self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server_socket.bind((self.host, self.port))
        self.udp_server_socket.setblocking(False)
        print(f"서버 대기 중... {self.host}:{self.port}")
        
    def __del__(self):
        self.server_socket.close()
        print("서버를 닫습니다..")

    def run(self):
        buffersize = 1024    
        
        print("UDP server is up and listening")

        while(True):
            try:
                byte_addr_pair = self.udp_server_socket.recvfrom(buffersize)
            except BlockingIOError:
                continue
            
            msg = byte_addr_pair[0]
            msg = msg.decode("utf-8")
            print(msg)   
            
            if self.msg_queue:
                self.msg_queue.put(msg)
            
            self.rcv_msg_signal.emit()
