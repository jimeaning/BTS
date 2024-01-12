#ifndef WEAPON_H
#define WEAPON_H

#include <string>

class Weapon {
public:
    Weapon(std::string _type, int servoPin);
    virtual ~Weapon();
    virtual void set_angle(int angle);
private:
    std::string _type;
    int angle;
    int servoPin_;
};
class For_Person : public Weapon {
public:
    For_Person(std::string _type, int servoPin);
    void set_angle(int angle) override;
};

class For_Vehicle : public Weapon {
public:
    For_Vehicle(std::string _type, int servoPin);
    void set_angle(int angle) override;
};

class For_Plane : public Weapon {
public:
    For_Plane(std::string _type, int servoPin);
    void set_angle(int angle) override;
};
#endif // WEAPON_H

