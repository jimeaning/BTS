#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>

#define GPIO_NUMBER "18" // GPIO 18 사용

// GPIO 핀 초기화 함수
void initializeGPIO(const std::string& pin) {
    // GPIO 핀 번호를 export 파일에 쓰기
    std::ofstream exportFile("/sys/class/gpio/export");
    exportFile << pin;
    exportFile.close();
    
    // 방금 export한 GPIO 핀을 출력으로 설정
    std::string gpioDirection = "/sys/class/gpio/gpio" + pin + "/direction";
    std::ofstream directionFile(gpioDirection.c_str());
    directionFile << "out";
    directionFile.close();
}

// LED 제어 함수
void controlLED(const std::string& pin) {
    std::string gpioValue = "/sys/class/gpio/gpio" + pin + "/value";
    while (true) {
        std::ofstream valueFile(gpioValue.c_str());
        valueFile << "1";
        valueFile.close();
        usleep(1000000); // 1초 대기

        valueFile.open(gpioValue.c_str());
        valueFile << "0";
        valueFile.close();
        usleep(1000000); // 1초 대기
    }
}

int main() {
    initializeGPIO(GPIO_NUMBER);
    controlLED(GPIO_NUMBER);

    return 0;
}