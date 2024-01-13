#include "stage.h"
#include <pigpio.h>
#include <unistd.h>
#include <iostream>

Stage::Stage()// : h_flag(1), start_index(0), steps(256), way_flag(0) 
    {
    // 생성자 초기화 리스트에서 h_flag 및 기타 멤버 변수 초기화
    
    if (gpioInitialise() < 0) {
        std::cout << "pigpio 초기화 실패\n";
    }
    else{
       for (int i=0; i < 4; ++i) {
        gpioSetMode(pin[i], PI_OUTPUT);}
    }
}

Stage::~Stage() {
    gpioTerminate();  // pigpio 정리
}

void Stage::rotateMotor() {
    int sequence[][4] = {{1, 0, 0, 1},
                         {1, 0, 0, 0},
                         {1, 1, 0, 0},
                         {0, 1, 0, 0},
                         {0, 1, 1, 0},
                         {0, 0, 1, 0},
                         {0, 0, 1, 1},
                         {0, 0, 0, 1}};

    while (true) {
        if (h_flag == 1) {
            if (way_flag == 0) {
                for (int i = start_index; i < steps; ++i) {
                    if (h_flag == 0) {
                        start_index = i;
                        break;
                    }

                    for (int j = 0; j < 8; ++j) {
                        for (int k = 0; k < 4; ++k) {
                            gpioWrite(pin[k], sequence[j][k]);
                        }
                        gpioDelay(2000);
                    }

                    if (i == (steps - 1)) {
                        start_index = 0;
                        way_flag = 1;
                    }
                }
            } 
	    else {
                for (int i = start_index; i < steps; ++i) {
                    if (h_flag == 0) {
                        start_index = i;
                        break;
                    }

                 for (int j = 7; j > -1; --j) {
                      for (int k = 0; k < 4; ++k) {
                            gpioWrite(pin[k], sequence[j][k]);
                            
                        }
                        gpioDelay(2000);
                    }

                    if (i == (steps - 1)) {
                        start_index = 0;
                        way_flag = 0;
                    }
                }
             
            }
        } else {

        }
    }
}

void Stage::flagChange()
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



