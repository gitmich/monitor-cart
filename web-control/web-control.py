# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move/<direction>/<action>')
def move(direction, action):
    if action == "down":
        print(f"Button {direction} pressed")
    elif action == "up":
        print(f"Button {direction} released")
    return f"{direction} button {action}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

