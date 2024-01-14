#ifndef STAGE_H
#define STAGE_H

#include <iostream>

class Stage {
public:
    Stage();  // 생성자
    ~Stage(); // 소멸자
    void rotateMotor();  // 함수 선언
    void flagChange();   // 함수 선언

private:
    int pin[4] = {17,18,27,22};
    int h_flag = 1;  // 멤버 변수
    int start_index = 0; // start_index 멤버 변수 추가
    int steps = 128; // steps 멤버 변수 추가
    int way_flag=0; // way_flag 멤버 변수 추가
};

#endif // STAGE_H
