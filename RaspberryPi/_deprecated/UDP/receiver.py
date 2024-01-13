import socket

server_ip = "10.10.15.102"
server_port = 3000
server_addr_port = (server_ip, server_port)
buffersize = 1024

udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_server_socket.bind(server_addr_port)
udp_server_socket.setblocking(False)

print("UDP server is up and listening")

while(True):
    try:
        byte_addr_pair = udp_server_socket.recvfrom(buffersize)
    except BlockingIOError:
        continue
    
    msg = byte_addr_pair[0]
    addr = byte_addr_pair[1]
    
    client_msg = "msg from client : {}".format(len(msg))
    client_ip = "client IP Addr : {}".format(addr)
    
    print(client_msg)
    print(client_ip)
    print(msg)
    
