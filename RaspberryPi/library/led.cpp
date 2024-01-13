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
			gpioSetMode(pin[i], PI_OUTPUT);
		}
    }
}

Led::~Led()
{
	gpioTerminate(); // 클래스 소멸 시 필요한 정리 작업 수행
}

void Led::ledWeapon(int pin_num)	// led -> pin[0]
{
	gpioWrite(pin_num, 1);
	std::cout << "Weapon LED On" << std::endl;
}
void Led::ledLaunch()
{
	gpioWrite(pin[3], 1);
	std::cout << "Launch LED On" << std::endl;
}
void Led::ledAllOff()
{
	for (int i = 0; i < 4; i++)
	{
		gpioWrite(pin[i], 0);
	}
	std::cout << "LED All Off" << std::endl;
}
