#include <iostream>
#include <pigpio.h>

#define SERVO_PIN 18
#define MIN_PULSE_WIDTH 500
#define MAX_PULSE_WIDTH 1500
#define STEP 10

int servo(int set_angle); // timesleep을 제어 할 파라미터 하나 추가

int servo(int set_angle) { 
    if (gpioInitialise() < 0) {
        std::cout << "pigpio initialization failed" << std::endl;
        return 1;
    }

    gpioSetMode(SERVO_PIN, PI_OUTPUT);

    while (true) { // while 문 XXXX if 문으로해서 조건 주기 앞에서 flag 넘어오면 실행
        for (int angle = 0; angle <= set_angle; angle += STEP) {
        
            int pulse = MIN_PULSE_WIDTH + (angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 90);
            gpioServo(SERVO_PIN, pulse);
            time_sleep(1); // 여기 나중에 파라미터 추가해서 발사 전까지 홀딩 할 수 있게 설정
        }

    }

    gpioTerminate();
}

int main() {
    servo(45); // 서보 함수 45도 설정값으로 동작
    return 0;
}
