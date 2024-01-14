#ifndef STAGE_H
#define STAGE_H

#include <iostream>

class Stage 
{
public:
    Stage();   
    ~Stage();
    void RotateMotor(); 
    void FlagChange(); 

private:
    int pin[4] = {17,18,27,22};
    int h_flag = 1;  
    int start_index = 0; 
    int steps = 128; 
    int way_flag=0; 
};

#endif // STAGE_H
