# app.py
from flask import Flask, render_template
import RPi.GPIO as GPIO
import motor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()

