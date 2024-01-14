#include "stage.h"
#include <pigpio.h>
#include <unistd.h>
#include <iostream>

Stage::Stage() 
{
    if (gpioInitialise() < 0) 
    {
        std::cout << "pigpio 초기화 실패\n";
    }
    else
    {
        for (int i=0; i < 4; ++i) 
	{
            gpioSetMode(pin[i], PI_OUTPUT);
	}
	std::cout << "stage 객체 생성" << std::endl;
    }
}

Stage::~Stage() 
{
    gpioTerminate();
    std::cout << "stage 객체 소멸" << std::endl;
}

void Stage::RotateMotor() 
{
    int sequence[][4] = 
    {    
	 {1, 0, 0, 1},
         {1, 0, 0, 0},
	 {1, 1, 0, 0},
	 {0, 1, 0, 0},
	 {0, 1, 1, 0},
	 {0, 0, 1, 0},
	 {0, 0, 1, 1},
	 {0, 0, 0, 1}
    };

    while (true) 
    {
        if (h_flag == 1) 
	{
            if (way_flag == 0) 
	    {
                for (int i = start_index; i < steps; ++i) 
		{
                    if (h_flag == 0) 
		    {
                        start_index = i;
                        break;
                    }
		    for (int j = 0; j < 8; ++j) 
		    {
                        for (int k = 0; k < 4; ++k) 
			{
                            gpioWrite(pin[k], sequence[j][k]);
                        }
                        gpioDelay(20000);
                    }
		    if (i == (steps - 1)) 
		    {
                        start_index = 0;
                        way_flag = 1;
                    }
                }
            } 
	    else 
	    {
                for (int i = start_index; i < steps; ++i) 
		{
                    if (h_flag == 0) 
		    {
                        start_index = i;
                        break;
                    }
		    for (int j = 7; j > -1; --j) 
		    {
                        for (int k = 0; k < 4; ++k) 
			{
                            gpioWrite(pin[k], sequence[j][k]);
                        }
                        gpioDelay(20000);
                    }
		    if (i == (steps - 1)) 
		    {
                        start_index = 0;
                        way_flag = 0;
                    }
                }
            }
        } 
	else 
	{
	    // 회전 멈춤
        }
    }
}

void Stage::FlagChange()
{
    if (h_flag == 1)
    {
        h_flag = 0;
    }
    else
    {
        h_flag = 1;
    }
}



