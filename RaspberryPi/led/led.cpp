#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>

#define GPIO_NUMBER "27" // GPIO 18 사용

int main() {
    // GPIO 핀 번호를 export 파일에 쓰기
    std::ofstream exportFile("/sys/class/gpio/export");
    exportFile << GPIO_NUMBER;
    exportFile.close();

    // 방금 export한 GPIO 핀을 출력으로 설정
    std::string gpioDirection = "/sys/class/gpio/gpio" + std::string(GPIO_NUMBER) + "/direction";
    std::ofstream directionFile(gpioDirection.c_str());
    directionFile << "out";
    directionFile.close();

    // GPIO 핀 값을 제어하여 LED 켜고 끄기
    std::string gpioValue = "/sys/class/gpio/gpio" + std::string(GPIO_NUMBER) + "/value";
    while (true) {
        // LED 켜기
        std::ofstream valueFile(gpioValue.c_str());
        valueFile << "1";
        valueFile.close();
        usleep(1000000); // 1초 대기

        // LED 끄기
        valueFile.open(gpioValue.c_str());
        valueFile << "0";
        valueFile.close();
        usleep(1000000); // 1초 대기
    }

    return 0;
}
