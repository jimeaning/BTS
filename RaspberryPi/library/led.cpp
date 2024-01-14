#include "led.h"
#include <pigpio.h>
#include <iostream>

Led::Led()
{
    if (gpioInitialise() < 0)
    {
        std::cout << "pigpio 초기화 실패\n";
    }
    else
    {
	for (int i = 0; i < 4; ++i)
	{
	    // pin 활성화
	    gpioSetMode(pin[i], PI_OUTPUT);
	}
	std::cout << "LED 객체 생성" << std::endl;
    }
}

Led::~Led()
{
    // pin 비활성화
    gpioTerminate();
    std::cout << "LED 객체 소멸" << std::endl;
}

void Led::LedWeapon(int pin_num)	// led -> pin[0]
{
    gpioWrite(pin_num, 1);
    std::cout << "Weapon LED On" << std::endl;
}
void Led::LedLaunch()
{
    gpioWrite(pin[3], 1);
    std::cout << "Launch LED On" << std::endl;
}
void Led::LedAllOff()
{
    for (int i = 0; i < 4; i++)
    {
	gpioWrite(pin[i], 0);
    }
    std::cout << "LED All Off" << std::endl;
}
