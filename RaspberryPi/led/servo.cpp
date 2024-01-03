#include <iostream>
#include <pigpio.h>

#define SERVO_PIN 18
#define MIN_PULSE_WIDTH 500
#define MAX_PULSE_WIDTH 1500
#define STEP 10

int main() {
    if (gpioInitialise() < 0) {
        std::cout << "pigpio initialization failed" << std::endl;
        return 1;
    }

    gpioSetMode(SERVO_PIN, PI_OUTPUT);

    while (true) {
        for (int angle = 0; angle <= 90; angle += STEP) {
            int pulse = MIN_PULSE_WIDTH + (angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 90);
            gpioServo(SERVO_PIN, pulse);
            time_sleep(1); // 1초 대기
        }

        for (int angle = 90; angle >= 0; angle -= STEP) {
            int pulse = MIN_PULSE_WIDTH + (angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 90);
            gpioServo(SERVO_PIN, pulse);
            time_sleep(1); // 1초 대기
        }
    }

    gpioTerminate();
    return 0;
}
