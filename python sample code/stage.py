class Stage:
    def __init__(self, h_flag):
        self.h_flag = h_flag
        print("Stage Class 실행")
        
    def __del__(self):
        print("Stage Class 종료")
        
    def rotate(self, running):
        print("rotate 함수 실행")
        while running:
            if self.h_flag == 1:
                pass
                # print("stage 도는 중.. ", self.h_flag)
            else:
                # print("stage 멈춤!! ", self.h_flag)
                break

        
    def flag_change(self):
        if self.h_flag == 1:
            self.h_flag = 0
        elif self.h_flag == 0:
            self.h_flag = 1
        print("flag_change 함수 실행")
        print("h_flag 값 : ", self.h_flag)
        # return self.h_flag