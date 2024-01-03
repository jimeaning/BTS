#include <stdio.h>
#include <pigpio.h>
#include <unistd.h>

#define STEPS 512 

int angleToSteps(float angle) {
    float steps = (angle / 360.0) * STEPS;
    return static_cast<int>(steps + 0.5);
}

// 모터를 회전시키는 함수
void rotateMotor(float angle) {
    if (gpioInitialise() < 0) {
        printf("pigpio 초기화 실패\n");
        return;
    }

    int pins[4] = {17, 18, 27, 22}; // ULN2003 드라이버에 연결된 GPIO 핀
    int sequence[][4] = {{1, 0, 0, 1},
                         {1, 0, 0, 0},
                         {1, 1, 0, 0},
                         {0, 1, 0, 0},
                         {0, 1, 1, 0},
                         {0, 0, 1, 0},
                         {0, 0, 1, 1},
                         {0, 0, 0, 1}};

    int steps = angleToSteps(angle); // 각도를 스텝으로 변환

    // 시계 방향으로 회전
    for (int i = 0; i < steps; ++i) {
        for (int j = 0; j < 8; ++j) {
            for (int k = 0; k < 4; ++k) {
                gpioWrite(pins[k], sequence[j][k]);
            }
            usleep(2000); // 적절한 딜레이 설정 (필요에 따라 조절)
        }
    }
    
    // 반시계 방향으로 회전하여 원래 위치로 복귀
    for (int i = 0; i < steps; ++i) {
        for (int j = 7; j >= 0; --j) {
            for (int k = 0; k < 4; ++k) {
                gpioWrite(pins[k], sequence[j][k]);
            }
            usleep(2000); // 적절한 딜레이 설정 (필요에 따라 조절)
        }
    }

    gpioTerminate();
}

int main() {
    float Angle = 90.0; // 회전할 각도
    rotateMotor(Angle); // 모터 회전 함수 호출

    return 0;
}

