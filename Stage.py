import RPi.GPIO as GPIO
import time
from collections import deque

# pin number, duration time
def led(pin, t):
    GPIO.setmode(GPIO.BOARD)    # set BOARD for control GPIO pin
    GPIO.setup(pin, GPIO.OUT)   # set pin's mode

    GPIO.output(pin, True)      
    time.sleep(t)

    GPIO.cleanup(pin)

# pin number, frequency, degree
def servoPos(pin, pwm, degree):
    SERVO_MAX_DUTY = 12
    SERVO_MIN_DUTY = 3

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    servo = GPIO.PWM(pin, pwm)  # Channel, frequency
    servo.start(0)  # pwm start

    if degree > 180:
        degree = 180

    try:
        while True :
            # duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
            # print("Degree : {} to {}(Duty)".format(degree, duty))
            servo.ChangeDutyCycle(12.0)     # change frequency
            time.sleep(3)
            servo.ChangeDutyCycle(3.0)
            time.sleep(3)
            # servo.stop()      # pwm stop
    except KeyboardInterrupt:
        GPIO.cleanup()
   
def stepMotor(pins):
    GPIO.setmode(GPIO.BOARD)
    stepPins = pins

    for pin in stepPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    sig = deque([1,0,0,0])
    step = 400
    dir = 1
    for pin in stepPins:
        GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)

    try:
        while True:
            for cnt in range(0, step):
                GPIO.output(stepPins[0], sig[0])
                GPIO.output(stepPins[1], sig[1])
                GPIO.output(stepPins[2], sig[2])
                GPIO.output(stepPins[3], sig[3])
                time.sleep(0.01)
                sig.rotate(dir)
            dir = dir * -1
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()



led(18, 3)
stepMotor([7, 11, 13, 15])
# servoPos(12, 50, 180)



