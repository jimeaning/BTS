class LED:
    def __init__(self):
        print("LED Class 실행")
        
    def __del__(self):
        print("LED Class 종료")
    
    def led_weapon(self, _type):
        print("{}번 LED Weapon 함수 실행".format(_type))
    
    def led_launch(self):
        print("LED Launch 함수 실행")
    
    def led_all_off(self):
        print("LED All Off 함수 실행")
