// weapon.cpp

#include "weapon.h"
#include <pigpio.h>
#include <iostream>

#define MIN_PULSE_WIDTH 500
#define MAX_PULSE_WIDTH 1500

Weapon::Weapon(std::string _type, int servo_pin) : _type(_type), servo_pin_(servo_pin) 
{
    if (gpioInitialise() < 0) 
	{
        std::cout << "pigpio initialization failed" << std::endl;
    }
   	else 
	{
        // pin 활성화
        gpioSetMode(servo_pin_, PI_OUTPUT);
        std::cout << "Weapon 객체 생성" << std::endl;
    }
}

Weapon::~Weapon() 
{
    // pin 비활성화
    gpioTerminate();
    std::cout << "Weapon 객체 소멸" << std::endl;
}

void Weapon::SetAngle(int angle) 
{
    int pulse = MIN_PULSE_WIDTH + (angle * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH) / 90);
    gpioServo(servo_pin_, pulse);
}

ForPlane::ForPlane(std::string _type, int servo_pin) : Weapon(_type, servo_pin) 
{
    std::cout << "For_Plane created!" << std::endl;
}
void ForPlane::SetAngle(int p_angle) 
{
    Weapon::SetAngle(p_angle); 
}

ForVehicle::ForVehicle(std::string _type, int servo_pin) : Weapon(_type, servo_pin) 
{
    std::cout << "For_Vehicle created!" << std::endl;
}
void ForVehicle::SetAngle(int v_angle) 
{
    Weapon::SetAngle(v_angle); 
}

ForPerson::ForPerson(std::string _type, int servo_pin) : Weapon(_type, servo_pin) 
{
    std::cout << "For_Person created!" << std::endl;
}
void ForPerson::SetAngle(int per_angle) 
{
    Weapon::SetAngle(per_angle); 
}
