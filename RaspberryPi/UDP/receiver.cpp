#include <iostream>
#include <cstring>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

#define SERVER_IP "10.10.15.102"
#define SERVER_PORT 3000
#define BUFFER_SIZE 1024

int main() {
    int sockfd;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t addrLen = sizeof(clientAddr);
    char buffer[BUFFER_SIZE];

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&serverAddr, 0, sizeof(serverAddr));
    memset(&clientAddr, 0, sizeof(clientAddr));

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);
    serverAddr.sin_port = htons(SERVER_PORT);

    bind(sockfd, (struct sockaddr *)&serverAddr, sizeof(serverAddr));

    std::cout << "UDP server is up and listening" << std::endl;

    while (true) {
        int len = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&clientAddr, &addrLen);

        if (len <= 0) {
            std::cout << "Failed to receive data" << std::endl;
        } else {
            buffer[len] = '\0';

            char clientMsg[100];
            sprintf(clientMsg, "msg from client: %d", len);

            char clientIP[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &clientAddr.sin_addr, clientIP, INET_ADDRSTRLEN);
            std::cout << clientMsg << std::endl;
            std::cout << "client IP Addr: " << clientIP << std::endl;
            std::cout << buffer << std::endl;
        }
    }

    close(sockfd);
    return 0;
}
