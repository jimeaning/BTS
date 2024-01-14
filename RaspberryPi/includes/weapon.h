#ifndef WEAPON_H
#define WEAPON_H

#include <string>

class Weapon
{
public:
    Weapon(std::string _type, int servo_pin);
    virtual ~Weapon();
    virtual void SetAngle(int angle);
private:
    std::string _type;
    int angle;
    int servo_pin_;
};

class ForPerson : public Weapon
{
public:
    ForPerson(std::string _type, int servo_pin);
    void SetAngle(int angle) override;
};

class ForVehicle : public Weapon
{
public:
    ForVehicle(std::string _type, int servo_pin);
    void SetAngle(int angle) override;
};

class ForPlane : public Weapon
{
public:
    ForPlane(std::string _type, int servo_pin);
    void SetAngle(int angle) override;
};
#endif // WEAPON_H

