# 尋人監控車

## Overview

## Required Components
### Software
- OS: Raspbian bullseye 64
- Python 3.9.2
- OpenCV 4.8.0-dev
### Hardware
- L298N X 1
- SG 90 X 1
- Gearmotor X 2
- HC-SR04 X 1
- Respberry Pi 4B X 1
- Pi Camera X 1
- Resistence X 1
- Car wheel X 2
- Car chassis X 1
- Hexagonal copper pillar X 8
- Battery case X 1
- Small breadboard X 1
- Tile board X 1

## Crafting
- Install SG90 and gearmotor on the car chassis.
![chassis.png](https://github.com/gitmich/monitor-cart/assets/4426184/1d6a60d8-ed4d-4ac3-9247-b90acd6123a0)
- Install hexagonal copper pillar on the car chassis.
![chassis1.png](https://github.com/gitmich/monitor-cart/assets/4426184/6fd3e41d-f73c-428d-8731-e19479a337a1)
- Install L298N on the car chassis.
![L298N-chassis.png](https://github.com/gitmich/monitor-cart/assets/4426184/e8945292-9b4a-4d1c-b275-e35d6b259792)
- Install HC-SR01 on the car chassis
![HC-SR01-chassis.png](https://github.com/gitmich/monitor-cart/assets/4426184/e96406a4-c765-47a5-9bd5-87505596c3ad)
- Install Raspberry Pi on the hexagonal copper pillar and set up the battery case under Pi
![22b224e9829f9cb63c988503917b1b17.png](https://github.com/gitmich/monitor-cart/assets/4426184/87d89c84-1636-4706-858d-ec46844a4942)
- Set up the small breadboard above the Raspberry pi
![df12bb87f897d7ea831faf6201cc8b3a.png](https://github.com/gitmich/monitor-cart/assets/4426184/ec5ccb66-8767-44e9-ae87-427fec3dc170)
- Set up the Pi Camera in front of the car chassis
![9791fdab8199be1e401db08f124cd86f.png](https://github.com/gitmich/monitor-cart/assets/4426184/3ae59e9c-2930-4624-bbee-e7f73cc9678b)
- Instal 4  hexagonal copper pillar under the PI and fixed tile board, then fixed the mobile power bank under the tile board.
![Completed_photo](https://github.com/gitmich/monitor-cart/assets/4426184/553d0897-b319-4870-9210-639ac5cab94e)

The photos of the completed assembly are as bellow:
![Completed_01](https://github.com/gitmich/monitor-cart/assets/4426184/f4905f06-63dc-453a-b332-4752c4cc9fe0)
![Completed_02](https://github.com/gitmich/monitor-cart/assets/4426184/4844642e-bc6c-4aa3-a5d6-6afac6161e0e)

The circuit diagram as bellow:
![wire-chart.jpg](https://github.com/gitmich/monitor-cart/assets/4426184/f437d882-4257-4227-a0d1-bda5cfac26a5)


## Cautions
- HC-SR04: 
	- This sensor sometimes gets extreme values, ex: more than 2 meters. You must filter out the extreme values, or your car will get disaster.
	- 
- L298N & motor: This project controls the wheel speed by calculating how many cm per second of the car. Then calculate the time of motor running we need.
- Since we need to slow the motor, we need to take off the jumpper from the L298N ENA and ENB. And connect the PWM pinout to ENA and ENB. 


## Environment prepare
### Enable Camera
- Config the raspberry
Run bellow command to enable camera
`sudo raspi-config`

Choice **3 Interface Options**
![raspi-config menu](https://github.com/gitmich/monitor-cart/assets/4426184/cb87d5bb-7eed-43e7-9d70-5e6950b7febb)

Choice **I1 Legacy Camera Enalbe/disable legacy camera support**
![Camera-option](https://github.com/gitmich/monitor-cart/assets/4426184/9a8bf456-a776-423c-81a1-f4791e00bd3f)

Choice **Yes** to enable Camera
![Camera-enable](https://github.com/gitmich/monitor-cart/assets/4426184/e99773ef-1eab-4eeb-bdb8-a2c55a3edad1)

Press **Esc** to exit the config menu


### Install opencv
1. Update the package
`sudo apt update && sudo apt upgrade -y`
2. Install CMack 3.14.4
```
cd ~/
wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4.tar.gz
tar xvzf cmake-3.14.4.tar.gz
cd ~/cmake-3.14.4
./bootstrap
make -j4
```
3. Install OpenCV
```
cd ~/
sudo apt install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libatlas-base-dev python3-scipy
git clone --depth 1 --branch 4.5.2-openvino https://github.com/opencv/opencv.git
cd opencv && mkdir build && cd build
cmake –DCMAKE_BUILD_TYPE=Release –DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
```

### Run Service
- Clone the source code from raspberry pi
`git clone https://github.com/gitmich/monitor-cart`
- Install python package
`pip install -r requirments.txt`
- Execute the server program
```
cd monitor-cart/web-control
python web-control.py
```

## UI Description
![UI](https://github.com/gitmich/monitor-cart/assets/4426184/668f0cab-3a62-4683-b143-961781ff00f7)

The upper part is the Pi Camera Live Stream. Users can watch the camera's view in this window.
The lower part consists of functional buttons. The Up, Down, Left, and Right buttons control the direction of the cart's movement. The central button enables the Tracking Mode. When Tracking Mode is enabled, the monitoring car will track people.

## Demo Video
https://github.com/gitmich/monitor-cart/assets/4426184/43cab267-4a0c-45ba-b141-e983f521368a



## Reference data
- Install OpenCV - https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA#Install-OpenCV
- Install OpenCV on Raspberry Pi - https://qengineering.eu/install-opencv-on-raspberry-pi.html
- Install OpenCV on your Raspberry Pi - https://raspberrypi-guide.github.io/programming/install-opencv#install-opencv-on-your-raspberry-pi
- OpenCV实践之路——行人检测 - https://blog.csdn.net/wc781708249/article/details/78589002
