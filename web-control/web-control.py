# app.py
from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import motor
import picamera
import threading
import io, time
import sg90
import numpy as np
import cv2

app = Flask(__name__)

frame = None
lock = threading.Lock()

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def generate_camera_stream():
    global frame
    with picamera.PiCamera() as camera:
        # set camera parameters
        camera.resolution = (640, 480)
        camera.rotation = 180
        #camera.framerate = 24
        time.sleep(2)  # wait for the camera to initialize

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
                # detect people in the image
                frame = np.frombuffer(frame, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame = cv2.resize(frame, (640, 480))
                (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
                boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                
                # get the biggest box
                if len(boxes) > 0:
                    max_box = boxes[0]
                    max_area = 0
                    for box in boxes:
                        area = (box[2] - box[0]) * (box[3] - box[1])
                        if area > max_area:
                            max_area = area
                            max_box = box
                    (xA, yA, xB, yB) = max_box
                    # draw the bounding box
                    cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                    # calculate the center of the box
                    center_x = (xA + xB) / 2
                    center_y = (yA + yB) / 2
                    # calculate the angle
                    angle_x = (center_x - 320) / 320 * 60
                    angle_y = (center_y - 240) / 240 * 60
                    # set the angle of the servo
                    sg90.set_servo_angle(90 + angle_x)
                    
                    # set the speed of the motor
                    # if angle_y > 0:
                    #     motor.forward()
                    #     motor.set_speed(100 - angle_y)
                    # else:
                    #     motor.backward()
                    #     motor.set_speed(100 + angle_y)
                else:
                    # motor.stop()
                    print('no people detected')

                # draw the bounding boxes
                for (xA, yA, xB, yB) in boxes:
                    cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                # encode as a jpeg image and return it
                ret, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
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

