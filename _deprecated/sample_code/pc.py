import socket

# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = ""
server_port = 3000
server_addr_port = (server_ip, server_port)

def send_indexes_to_server(c_index, d_index):
    # 메시지 생성
    msg_to_send = f"c_index: {c_index}, d_index: {d_index}"
    bytes_to_send = str.encode(msg_to_send)

    # 소켓을 UDP로 열고 서버의 IP/Port로 메시지를 보냄
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.sendto(bytes_to_send, server_addr_port)
    print(f"Sent message to server: {msg_to_send}")
    
def detect_target(image):
    print("target detect")
    target = [(100, 120, 200, 250)] 
    d_index = 1
    return d_index

def classify_target(d_index):
    print("target classify")
    c_index = 2
    return c_index

# detect_target 함수 호출
d_index = detect_target("sample_image")

# classify_target 함수 호출
c_index = classify_target(d_index)

send_indexes_to_server(c_index, d_index)