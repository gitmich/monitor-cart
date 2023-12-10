import RPi.GPIO as GPIO
import time

def init_motor():
    # 設置 GPIO 針腳模式為 BCM
    GPIO.setmode(GPIO.BCM)
    # 定義 L298N 的 GPIO 針腳
    Motor1A = 17
    Motor1B = 18
    Motor2A = 23
    Motor2B = 22

    # 設置馬達的 GPIO 針腳為輸出模式
    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor2A, GPIO.OUT)
    GPIO.setup(Motor2B, GPIO.OUT)

def close_motor():
    GPIO.cleanup()
   

def forward():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def backward():
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


def stop():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.LOW)

if __name__ == '__main__':
    try:
        while True:
            cmd = input("Enter '1' to move forward, '2' to move backward: ")
            if cmd == '1':
                forward(3)
            elif cmd == '2':
                backward(3)

    except KeyboardInterrupt:
        GPIO.cleanup()

