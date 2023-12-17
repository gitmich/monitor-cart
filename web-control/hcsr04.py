import RPi.GPIO as GPIO
import time

def init_hcsr04():
    global TRIG
    global ECHO
    # 使用 GPIO 針腳編號
    GPIO.setmode(GPIO.BCM)
    
    # 設定 GPIO 針腳
    TRIG = 24  # 用於發送信號
    ECHO = 25  # 用於接收信號
    
    # 設定 GPIO 的工作方式 (IN / OUT)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
def close_hcsr04():
    GPIO.cleanup()

def distance():
    global TRIG
    global ECHO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # 發送高電平信號到 TRIG
    GPIO.output(TRIG, True)
    # 保持信號 10 us
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    # 紀錄發送信號的時間
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        if start_time - stop_time > 1:
            print("Sending Time out")
            break


    # 紀錄接收到回聲的時間
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        if stop_time - start_time > 1:
            print("Receiving Time out")
            break


    # 計算回聲的時間差
    time_elapsed = stop_time - start_time
    # 聲音速度 (34300 cm/s) 乘以時間差，然後除以 2 (來回距離)
    distance = (time_elapsed * 34300) / 2

    return distance

if __name__ == "__main__":
    try:
        init_hcsr04()
        while True:
            dist = distance()
            print(f"Distance: {dist:.2f} cm")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    
