# app.py
from flask import Flask, render_template, Response, jsonify
import RPi.GPIO as GPIO
import motor
import picamera
import threading
import io, time
import sg90, hcsr04
import numpy as np
import cv2

app = Flask(__name__)

frame = None
camera_thread_lock = threading.Lock()
distance = 0
distance_lock = threading.Lock()
scan_distance_time = time.time()
get_aim_distance_running = False
tracking_mode = False


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
            with camera_thread_lock:
                stream.seek(0)
                frame = stream.read()
            stream.seek(0)
            stream.truncate()

@app.route('/')
def index():
    return render_template('index.html')

def measure_distance_continuously():
    global distance
    while True:
        # 測量距離的代碼...
        new_distance = hcsr04.distance()

        with distance_lock:
            distance = new_distance

        time.sleep(0.5)  # 或根據需要調整延遲時間

def check_distance():
    global distance
    min_distance = 30
    max_distance = 50
    limit_distance = 100
    # speed: 18 cm/sec
    speed = 18
    
    with distance_lock:
        if distance < min_distance:
            print(f"distance: {distance:.2f}")
            print(f"min_distance: {min_distance:.2f}")
            move_time = (min_distance - distance)/speed
            print(f"backward move_time: {move_time:.2f}")
            motor.backward()
            time.sleep(move_time)
            motor.stop()
        elif distance > max_distance and distance < limit_distance:
            print(f"distance: {distance:.2f}")
            print(f"max_distance: {max_distance:.2f}")
            move_time = (distance - max_distance)/speed
            print(f"forward move_time: {move_time:.2f}")
            motor.forward()
            time.sleep(move_time)
            motor.stop()
        else:
            print(f"distance: {distance:.2f}")
            print("stop.........")
            motor.stop()
    time.sleep(0.1)

def get_aim_distance(xA, yA, xB, yB):
    global scan_distance_time
    global get_aim_distance_running
    global distance
    
    get_aim_distance_running = True
    # calculate the center of the box
    center_x = (xA + xB) / 2
    center_y = (yA + yB) / 2
    # calculate the angle
    angle_x = (center_x - 320) / 320 * 30
    angle_y = (center_y - 240) / 240 * 30
    # get the distance from the ultrasonic sensor every 3 seconds
    if time.time() - scan_distance_time > 3:
        # set the angle of the servo
        sg90.set_servo_angle(90 - angle_x)
        scan_distance_time = time.time()
        dist = hcsr04.distance()
        print(f"Distance: {dist:.2f} cm")
        with distance_lock:
            distance = dist
        
        if abs(angle_x) > 10:
            print(f"angle_x: {angle_x:.2f}")
            motor.look_target(angle_x)
            sg90.set_servo_angle(90)
        
        check_distance()
        
    get_aim_distance_running = False

def stream():
    global frame
    global get_aim_distance_running
    threshold = 0.75
    while True:
        # reset box and weight
        boxes = []
        max_box = []
        max_weight = 0
        
        with camera_thread_lock:
            if frame:
                # detect people in the image
                frame = np.frombuffer(frame, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frame = cv2.resize(frame, (640, 480))
                
                # -----
                if tracking_mode == True:
                    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
                    # (rects, weights) = hog.detectMultiScale(frame, winStride=(6, 6),padding=(6, 6), scale=1.1)
                    # filter the target with low confidence
                    filtered_rects = [rect for rect, weight in zip(rects, weights) if weight > threshold]
                    # boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in filtered_rects])
                    
                    # get the biggest box and weight
                    if len(boxes) > 0:
                        # max_box = boxes[0]
                        # max_weight = 0
                        for box, weight in zip(boxes, weights):
                            if weight > max_weight:
                                max_weight = weight
                                max_box = box
                        (xA, yA, xB, yB) = max_box
                        # draw the bounding box
                        # cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                        # draw the weight
                        # aim the target and get the distance from the ultrasonic sensor
                        if get_aim_distance_running == False:
                            get_aim_distance_threading =  threading.Thread(target=get_aim_distance, args=(xA, yA, xB, yB))
                            get_aim_distance_threading.start()
                    else:
                        # motor.stop()
                        # print('no people detected')
                        i = 1
                    
                    # if the max_box is not empty then draw the bounding box and weight
                    if len(max_box) > 0:
                        # print(f"len(max_box): {len(max_box)}")
                        (xA, yA, xB, yB) = max_box
                        # draw the bounding box
                        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                        # draw the weight
                        cv2.putText(frame, f"{max_weight:.2f}", (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # -----
                
                # encode as a jpeg image and return it
                ret, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
        time.sleep(0.1)
    get_aim_distance_threading.join()
    


@app.route('/video_feed')
def video_feed():
    return Response(stream(),mimetype='multipart/x-mixed-replace; boundary=frame')
    # return 0


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

@app.route('/toggle_tracking')
def toggle_tracking():
    global tracking_mode
    tracking_mode = not tracking_mode
    print(f"tracking_mode: {tracking_mode}")
    return jsonify({'tracking_mode': tracking_mode})


if __name__ == '__main__':
    try:
        camera_thread = threading.Thread(target=generate_camera_stream)
        camera_thread.start()
        motor.init_motor()
        sg90.init_servo()
        hcsr04.init_hcsr04()
        sg90.set_servo_angle(90)
        #dis = hcsr04.distance()
        #print(dis)
        #app.run(host='0.0.0.0', port=5000, debug=True)
        app.run(host='0.0.0.0', port=5000)
        #time.sleep(5)
    except Exception as e:
        print(e)
        GPIO.cleanup()
        sg90.close_servo()
        motor.close_motor()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sg90.close_servo()
        motor.close_motor()

