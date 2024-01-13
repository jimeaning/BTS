class Led
{
public:
    Led();  // 생성자
    ~Led(); // 소멸자
    void ledWeapon(int pin_num);  // 함수 선언
    void ledLaunch();   // 함수 선언
    void ledAllOff();   // 함수 선언
    int pin[4] = {23,24,25,8};
};
