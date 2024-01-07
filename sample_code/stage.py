import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
pins = [17, 18, 27, 22]
sequence = [[1, 0, 0, 1],
			[1, 0, 0, 0],
			[1, 1, 0, 0],
			[0, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 0, 1, 0],
			[0, 0, 1, 1],
			[0, 0, 0, 1]]

STEPS = 512
GPIO.setmode(GPIO.BCM)
for pin in pins:
	GPIO.setup(pin, GPIO.OUT)



# 각도를 스텝으로 변환하는 함수
def angle_to_steps(angle):
	steps = (angle / 360.0) * STEPS
	return int(steps + 0.5)

# 모터를 회전시키는 함수
def rotate_motor(angle):

	steps = angle_to_steps(angle)

	try:
		# 왕복 운동을 위한 루프
		# 0에서 180도까지 회전
		for i in range(steps):
			print(i)
			for j in range(8):
				for k in range(4):
					GPIO.output(pins[k], sequence[j][k])
				time.sleep(0.002)  # 적절한 딜레이 설정 (필요에 따라 조절)

		# 180에서 0도까지 회전하여 원래 위치로 복귀
		for i in range(steps):
			print("reverse",i)
			for j in range(7, -1, -1):
				for k in range(4):
					GPIO.output(pins[k], sequence[j][k])
				time.sleep(0.002)  # 적절한 딜레이 설정 (필요에 따라 조절)

	except KeyboardInterrupt:
		pass

	

# 모터를 멈추는 함수
def stop_motor():
	for pin in pins:
		GPIO.output(pin, GPIO.LOW)  # 모든 핀을 LOW로 설정하여 모터 정지

class Stage:
	def __init__(self, h_flag):
		self.h_flag = h_flag	# 0 : stop | 1 : go
		self.way_flag = 0		# 0 : forward | 1 : backward
		self.start_index = 0	# step start index
		self.steps = angle_to_steps(180.0)
		print("Stage Class 실행")
		
	def __del__(self):
		GPIO.cleanup()
		print("Stage Class 종료")
		
	def rotate(self):
		
		print("rotate 함수 실행")
		while True:
			if self.h_flag == 1:
				if self.way_flag == 0:
					for i in range(self.start_index, self.steps):	
						if self.h_flag == 0:	
							self.start_index = i
							break			
						for j in range(8):
							for k in range(4):
								GPIO.output(pins[k], sequence[j][k])
							time.sleep(0.002)  # 적절한 딜레이 설정 (필요에 따라 조절)
						if i == (self.steps - 1):
							self.start_index = 0
							self.way_flag = 1		
					print("way", self.way_flag)

				else:
					
					for i in range(self.start_index, self.steps):
						if self.h_flag == 0:
							self.start_index = i
							break
						for j in range(7, -1, -1):
							for k in range(4):
								GPIO.output(pins[k], sequence[j][k])
							time.sleep(0.002)  # 적절한 딜레이 설정 (필요에 따라 조절)
						if i == (self.steps - 1):
							self.start_index = 0
							self.way_flag = 0
			else:
				print("stage 멈춤!! ", self.h_flag)
		
	def flag_change(self):
		if self.h_flag == 1:
			self.h_flag = 0
		elif self.h_flag == 0:
			self.h_flag = 1
		print("flag_change 함수 실행")
		print("h_flag 값 : ", self.h_flag)
		# return self.h_flag
