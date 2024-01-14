class Led
{
public:
    Led();  
    ~Led(); 
    void LedWeapon(int pin_num);  
    void LedLaunch();   
    void LedAllOff();   
    int pin[4] = {23,24,25,8};
};
