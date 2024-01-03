#include <iostream>
#include <pigpio.h>

#define STEPS_PER_REVOLUTION 2048 // 28BYJ-48 모터의 한 바퀴 스텝 수
#define ANGLE 180 // 움직일 각도
#define DELAY_MICROSECONDS 3000 // 스텝 간의 간격(마이크로초 단위)
#define DIRECTION_PIN 23 // 방향을 제어하는 GPIO 핀 번호

// 28BYJ-48 모터의 시퀀스 배열
const int sequence[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 0, 1},
    {1, 0, 0, 1}
};

int main() {
    if (gpioInitialise() < 0) {
        std::cout << "pigpio initialization failed" << std::endl;
        return 1;
    }

    // 모터 제어에 사용되는 GPIO 핀 설정
    int pins[4] = {17, 18, 27, 22}; // ULN2003 드라이버에 연결된 GPIO 핀

    for (int i = 0; i < 4; ++i) {
        gpioSetMode(pins[i], PI_OUTPUT);
    }
    
    // 방향 제어 핀 설정
    gpioSetMode(DIRECTION_PIN, PI_OUTPUT);

    int steps = (STEPS_PER_REVOLUTION * ANGLE) / 360; // 움직일 스텝 수
    int step_delay = DELAY_MICROSECONDS;

    while (true) {
        // 한 방향으로 회전
        gpioWrite(DIRECTION_PIN, 0);
        for (int i = 0; i < steps; ++i) {
            for (int j = 0; j < 8; ++j) {
                for (int k = 0; k < 4; ++k) {
                    gpioWrite(pins[k], sequence[j][k]);
                }
                gpioDelay(step_delay);
            }
        }
        gpioDelay(500000); // 모터 정지를 위한 지연

        // 반대 방향으로 회전
        gpioWrite(DIRECTION_PIN, 1);
        for (int i = 0; i < steps; ++i) {
            for (int j = 7; j >= 0; --j) {
                for (int k = 0; k < 4; ++k) {
                    gpioWrite(pins[k], sequence[j][k]);
                }
                gpioDelay(step_delay);
            }
        }
        gpioDelay(500000); // 모터 정지를 위한 지연
    }

    gpioTerminate();
    return 0;
}

