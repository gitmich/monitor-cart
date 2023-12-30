import RPi.GPIO as GPIO
import time

# The motor speed: 18 cm/sec
angle_speed = 3
pwn = None
motor_speed = 30

def init_motor():
    global pwm
    global Motor1A, Motor1B, Motor2A, Motor2B
    # 設置 GPIO 針腳模式為 BCM
    GPIO.setmode(GPIO.BCM)
    # 定義 L298N 的 GPIO 針腳
    Motor1A = 17
    Motor1B = 18
    Motor2A = 23
    Motor2B = 22
    Motor_PWM = 12

    # 設置馬達的 GPIO 針腳為輸出模式
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor2A, GPIO.OUT)
    GPIO.setup(Motor2B, GPIO.OUT)
    GPIO.setup(Motor_PWM, GPIO.OUT)
    
    pwm = GPIO.PWM(Motor_PWM, 1000)
    pwm.start(0)
    pwm.ChangeDutyCycle(motor_speed)

def close_motor():
    GPIO.cleanup()
   

def forward():
    global motor_speed
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def backward():
    global motor_speed
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def left():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def right():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def left_angle(angle):
    global angle_speed
    move_time = angle / 360 * angle_speed
    print(f"left move_time: {move_time}")
    left()
    time.sleep(move_time)
    stop()
    
def right_angle(angle):
    global angle_speed
    move_time = angle / 360 * angle_speed
    print(f"right move_time: {move_time}")
    right()
    time.sleep(move_time)
    stop()
    
def look_target(angle):
    if angle < 0:
        print("left")
        left_angle(abs(angle))
    else:
        print("right")
        right_angle(abs(angle))

def stop():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.LOW)

if __name__ == '__main__':
    try:
        init_motor()
        while True:
            cmd = input("Enter '1' to move forward, '2' to move backward: ")
            if cmd == '1':
                forward()
                time.sleep(1)
                stop()
            elif cmd == '2':
                backward()
                time.sleep(1)
                stop()
            elif cmd == '3':
                motor_speed = motor_speed + 10
                print(f"motor_speed: {motor_speed}")
            elif cmd == '4':
                motor_speed = motor_speed - 10
                print(f"motor_speed: {motor_speed}")

    except KeyboardInterrupt:
        GPIO.cleanup()

