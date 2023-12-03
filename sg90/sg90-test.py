import RPi.GPIO as GPIO
import time

# 設置伺服馬達的 GPIO 針腳
servo_pin = 15  # 伺服馬達信號線連接的 GPIO 針腳
GPIO.setmode(GPIO.BCM)  # 使用 Broadcom 針腳編號
GPIO.setup(servo_pin, GPIO.OUT)

# 在伺服馬達針腳上設置 50Hz 的 PWM（20ms PWM 週期）
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)  # 以 0% 的占空比啟動 PWM

def set_servo_angle(angle):
    # 將輸入的角度轉換為對應的占空比
    duty_cycle = angle / 18.0 + 2
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        # 請使用者輸入一個角度
        angle = float(input('請輸入一個 0 到 180 之間的角度: '))
        set_servo_angle(angle)
        time.sleep(1)  # 等待 1 秒讓伺服馬達到達指定位置
except KeyboardInterrupt:
    pwm.stop()  # 停止 PWM
    GPIO.cleanup()  # 在 CTRL+C 退出時清理 GPIO

