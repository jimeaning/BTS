#include "weapon.h"
#include "stage.h"
#include "led.h"

#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <thread>

#define SERVER_IP "10.10.15.102"
#define SERVER_PORT 3000
#define BUFFER_SIZE 1024
#define GUI_IP "10.10.15.106"
#define GUI_PORT 4000

char buffer[BUFFER_SIZE];
int object_index = -1;
int flag = -1; 

void HandleUDP()
{
    int sockfd;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t addrLen = sizeof(clientAddr);
    
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&serverAddr, 0, sizeof(serverAddr));
    memset(&clientAddr, 0, sizeof(clientAddr));

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);
    serverAddr.sin_port = htons(SERVER_PORT);

    bind(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr));

    std::cout << "UDP server is up and listening" << std::endl;

    while (true)
    {
        int len = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&clientAddr, &addrLen);
 
        if (len <= 0)
	{
            std::cout << "Failed to receive data" << std::endl;
        }
	else
	{
            buffer[len] = '\0';
	    char clientMsg[100];
            std::cout << "메시지 수신 :  " << buffer << std::endl;
	    
	    if (strcmp(buffer, "0") == 0)
	    {
           	object_index = 0;
	    } 
	    else if (strcmp(buffer, "1") == 0)
	    {
	        object_index = 1;
	    }
       	    else if (strcmp(buffer, "2") == 0)
	    {
                object_index = 2;
	    }
       	    else if (strcmp(buffer, "3") == 0)
	    {
                object_index = 3;
	    }
       	    else if (strcmp(buffer, "4") == 0)
	    {
                object_index = 4;
	    }
       	    else if (strcmp(buffer, "5") == 0)
	    {
                object_index = 5;
	    }
       	    else if (strcmp(buffer, "6") == 0)
	    {
                object_index = 6;
	    }
	}
    }

    close(sockfd);
}

int main()
{
    int gui_sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(GUI_PORT);
    inet_pton(AF_INET, GUI_IP, &(serverAddress.sin_addr));
    
    connect(gui_sockfd, (struct sockaddr *)&serverAddress, sizeof(serverAddress));
    
    // 객체 생성
    Stage* stage = new Stage();
    Led* led = new Led();
    Weapon* weapon = nullptr;
    
    // 쓰레드 생성 및 실행
    std::thread udpThread(HandleUDP);
    std::thread stageThread(&Stage::RotateMotor, stage);
    
    while (true)
    {
	//weapon 객체 생성 
	if (weapon == nullptr && buffer[0] != '\0')
	{
	    if (object_index == 0)
	    {
		weapon = new ForPerson("0", 5);
		led -> LedWeapon(led -> pin[0]);
		std::string message = "전방에 사람 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	    else if (object_index == 1)
	    {
		weapon = new ForVehicle("0", 6);
		led -> LedWeapon(led -> pin[1]);
		std::string message = "전방에 레토나 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	    else if (object_index == 2)
	    {
		weapon = new ForVehicle("1", 6);
		led -> LedWeapon(led -> pin[1]);
		std::string message = "전방에 두돈반 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	    else if (object_index == 3)
	    {
		weapon = new ForVehicle("2", 6);
		led -> LedWeapon(led -> pin[1]);
		std::string message = "전방에 탱크 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }          
	    else if (object_index == 4)
	    {
		weapon = new ForPlane("0", 13);
		led -> LedWeapon(led -> pin[2]);
		std::string message = "전방에 수송기 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	    else if (object_index == 5)
	    {
		weapon = new ForPlane("1", 13);
		led -> LedWeapon(led -> pin[2]);
		std::string message = "전방에 헬리콥터 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	    else if (object_index == 6)
	    {
		weapon = new ForPlane("2", 13);
		led -> LedWeapon(led -> pin[2]);
		std::string message = "전방에 전투기 발견!";
		send(gui_sockfd, message.c_str(), message.size(), 0);
	    }
	}
	
	// stage 멈춤
        if (strcmp(buffer, "9") == 0)
	{
	    stage -> FlagChange();
	    flag = 0;
	    std::string message = "타겟 포착";
	    send(gui_sockfd, message.c_str(), message.size(), 0);
	    memset(buffer, 0, sizeof(buffer));
	}
	
	// 포 각도 조절
	if (flag == 0 && buffer[0] != '\0')
	{
	    int angle = std::stoi(buffer);
	    sleep(2);
	    angle = 90 - angle;
	    weapon -> SetAngle(angle);
	    std::string message = "포 정렬";
	    send(gui_sockfd, message.c_str(), message.size(), 0);
	    sleep(1);
	    flag = 1;
	}
	
	// 발사 준비 완료
	if (flag == 1)
	{
	    led -> LedLaunch();
	    flag=2;
	    std::string message = "발사 준비 완료";
	    send(gui_sockfd, message.c_str(), message.size(), 0);
	}
	
	// 발사 완료
	if(strcmp(buffer, "발사") == 0 && flag == 2)
	{
	    sleep(3);
	    weapon -> SetAngle(90);
	    led -> LedAllOff();
	    memset(buffer, 0, sizeof(buffer));
	    //delete weapon;
	    weapon = nullptr;
	    object_index = -1;
	    flag = -1;
	    stage -> FlagChange();
	    std::string message = "발사 완료. 시스템 재개";
	    send(gui_sockfd, message.c_str(), message.size(), 0);
	}
    }
    
    close(gui_sockfd);
    
    // 스레드 종료 대기
    udpThread.join();
    stageThread.join();
    
    // 객체 소멸
    delete weapon;
    delete led;

    return 0;
}
