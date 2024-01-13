// weapon.cpp

#include "weapon.h"
#include <pigpio.h>
#include <iostream>

//#define SERVO_PIN 18
#define MIN_PULSE_WIDTH 500
#define MAX_PULSE_WIDTH 1500
//#define STEP 10

Weapon::Weapon(std::string _type, int servoPin) : _type(_type), servoPin_(servoPin) {
    if (gpioInitialise() < 0) {
        std::cout << "pigpio initialization failed" << std::endl;
    } else {
        gpioSetMode(servoPin_, PI_OUTPUT);
    }
}

Weapon::~Weapon() {
    gpioTerminate(); // 클래스 소멸 시 필요한 정리 작업 수행
}

void Weapon::set_angle(int angle) {
    //for (int loopAngle = 0; loopAngle <= angle; loopAngle += STEP) {
        int pulse = MIN_PULSE_WIDTH + (angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 90);
        gpioServo(servoPin_, pulse);
        time_sleep(1);
    //}
}

For_Plane::For_Plane(std::string _type, int servoPin) : Weapon(_type, servoPin) {
        std::cout << "For_Plane created!" << std::endl;
}
void For_Plane::set_angle(int set_angle) {
    // For_Vehicle에 특화된 동작 추가
    Weapon::set_angle(set_angle); // 기존 동작은 부모 클래스의 동작 그대로 사용
}
For_Vehicle::For_Vehicle(std::string _type, int servoPin) : Weapon(_type, servoPin) {
        std::cout << "For_Vehicle created!" << std::endl;
}

void For_Vehicle::set_angle(int set_angle) {
    // For_Vehicle에 특화된 동작 추가
    Weapon::set_angle(set_angle); // 기존 동작은 부모 클래스의 동작 그대로 사용
}
For_Person::For_Person(std::string _type, int servoPin) : Weapon(_type, servoPin) {
        std::cout << "For_Person created!" << std::endl;
}
void For_Person::set_angle(int set_angle) {
    // For_Vehicle에 특화된 동작 추가
    Weapon::set_angle(set_angle); // 기존 동작은 부모 클래스의 동작 그대로 사용
}
