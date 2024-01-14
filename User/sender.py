import socket


"""발사 버튼 클릭 후 HW에 '발사' sign 보내는 메서드"""
def SendMsg():
    server_ip = "10.10.15.102"
    server_port = 3000
    server_addr_port = (server_ip, server_port)

    msg_from_client = "발사"
    bytes_to_send = str.encode(msg_from_client)

    # UDP 통신
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_client_socket.sendto(bytes_to_send, server_addr_port)
    print(msg_from_client)
