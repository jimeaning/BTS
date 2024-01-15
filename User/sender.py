"""
발사 버튼 통신을 위한 모듈
"""
import socket


# 서버 설정
host = "10.10.15.102"
port = 3000


class SendMessage():
    """발사 버튼 통신을 위한 클래스"""
    def __init__(self):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __del__(self):
        self.client_socket.close()
        print("SendMsg 객체 사라집니다")

    def SendMsg(self):
        """발사 버튼 클릭 후 HW에 '발사' sign 보내는 메서드"""
        msg_from_client = "발사"
        
        bytes_to_send = str.encode(msg_from_client)    
        self.client_socket.sendto(bytes_to_send, (self.host, self.port))
        
        print(msg_from_client)
