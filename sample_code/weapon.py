class Weapon:
    def __init__(self, _type):
        self._type = _type

    def set_angle(self, angle):
        self.angle = angle
        print("세로 방향으로 포대 각도 조절")

# Plane 클래스 - Weapon 클래스를 상속
class For_Plane(Weapon):
    def __init__(self, _type):
        super().__init__(_type)
        print("plane 생성")

# Tank 클래스 - Weapon 클래스를 상속
class For_Vehicle(Weapon):
    def __init__(self, _type):
        super().__init__(_type)
        print("vehicle 생성")

# Person 클래스 - Weapon 클래스를 상속
class For_Person(Weapon):
    def __init__(self, _type):
        super().__init__(_type)
        print("person 생성")