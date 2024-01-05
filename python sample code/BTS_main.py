import threading
import time
from stage import Stage
from weapon import *
from led import LED

import time
import socket

server_ip = ""
server_port = 7006
server_addr_port = (server_ip, server_port)
buffersize = 1024

udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_server_socket.bind(server_addr_port)
udp_server_socket.setblocking(False)

h_flag = 1

s = Stage(h_flag)
index = -1
running = True


# 스레드에서 실행될 함수
def thread_UDP():
    global index
    while running:
        try:
            byte_addr_pair = udp_server_socket.recvfrom(buffersize)
        except BlockingIOError:
            continue
        
        msg = byte_addr_pair[0]
        
        result = msg.decode('utf-8')

        if result == "9":
            s.flag_change()
        elif result == "0":
            index = 0
        elif result == "1":
            index = 1
        elif result == "2":
            index = 2
        elif result == "3":
            index = 3
        elif result == "4":
            index = 4
        elif result == "5":
            index = 5
        elif result == "6":
            index = 6


def main():    
    global index
    global running

    # 스레드 생성
    thread1 = threading.Thread(target=s.rotate, args=(running, ))
    thread2 = threading.Thread(target=thread_UDP)

    # 스레드 시작
    thread1.start()
    thread2.start()
    
    # while 루프를 통해 계속해서 작업을 반복
    
    while running:
        ''' When stage stop'''
        if s.h_flag == 0:
            
            ''' Create Object'''
            # Human
            if index == 0:
                weapon = For_Person(0)
            # Two-Half
            elif index == 1:
                weapon = For_Vehicle(0)
            # Retona
            elif index == 2:
                weapon = For_Vehicle(1)
            # Tank
            elif index == 3:
                weapon = For_Vehicle(2)
            # Airplane
            elif index == 4:
                weapon = For_Plane(0)
            # Hellicopter
            elif index == 5:
                weapon = For_Plane(1)
            # Fighter
            elif index == 6:
                weapon = For_Plane(2)
            print("WEApon", weapon)
            
            led = LED()
            

            if weapon.__class__.__name__ == "For_Person":
                print("z")
                led.led_weapon(0)
            elif weapon.__class__.__name__ == "For_Vehicle":
                print("x")
                led.led_weapon(1)
            else:
                print("c")
                led.led_weapon(2)
            
            weapon.set_angle(90)

            led.led_launch()

            led.led_all_off()

            weapon.set_angle(0)

            s.flag_change()

            del weapon
            del led

            index = -1
            running = False
            s.rotate(running)
            time.sleep(3)     

    # 스레드 종료 대기
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()  # 위에서 정의한 main 함수 호출

