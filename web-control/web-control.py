# app.py
from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import motor
import picamera
import threading
import io, time
import sg90

app = Flask(__name__)

frame = None
lock = threading.Lock()


def generate_camera_stream():
    global frame
    with picamera.PiCamera() as camera:
        # 設置相機參數
        camera.resolution = (640, 480)
        camera.rotation = 180
        #camera.framerate = 24
        time.sleep(2)  # 讓相機預熱

        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            with lock:
                stream.seek(0)
                frame = stream.read()
            stream.seek(0)
            stream.truncate()

@app.route('/')
def index():
    return render_template('index.html')

def stream():
    global frame
    while True:
        with lock:
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1) 


@app.route('/video_feed')
def video_feed():
    return Response(stream(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move/<direction>/<action>')
def move(direction, action):
    if action == "down":
        print(f"Button {direction} pressed")
        if direction == "up":
            motor.forward()
        elif direction == "down":
            motor.backward()
        elif direction == "left":
            motor.left()
        elif direction == "right":
            motor.right()
    elif action == "up":
        print(f"Button {direction} released")
        print("stop.........")
        motor.stop()
    return f"{direction} button {action}"


if __name__ == '__main__':
    try:
        t = threading.Thread(target=generate_camera_stream)
        t.start()
        motor.init_motor()
        sg90.init_servo()
        sg90.set_servo_angle(90)
        #app.run(host='0.0.0.0', port=5000, debug=True)
        app.run(host='0.0.0.0', port=5000)
        time.sleep(5)
        sg90.set_servo_angle(130)

    except Exception as e:
        print(e)
        GPIO.cleanup()
        sg90.close_servo()
        motor.close_motor()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sg90.close_servo()
        motor.close_motor()

