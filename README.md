# 尋人監控車

## Overview

## Required Components
### Software
- OS: 
- Python
- OpenCV
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
- Hexagonal copper pillar X 4
- Battery case X 1
- Small breadboard X 1
### Tools

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

The circuit diagram as bellow:
![wire-chart.jpg](https://github.com/gitmich/monitor-cart/assets/4426184/46612d9f-4486-4073-b1c9-cc6325b57425)

The photos of the completed assembly are as bellow:
![b521a488329e4f7c961b3924a37a96d1](https://github.com/gitmich/monitor-cart/assets/4426184/34ee4fa1-ae28-4e11-b2c9-dcc575645600)


![d2843a0b2b214743a1efd255ea4bf60e](https://github.com/gitmich/monitor-cart/assets/4426184/b234f590-e84d-4d57-a73e-2f10afd6f143)

## Cautions
- HC-SR04: 
	- This sensor sometimes gets extreme values, ex: more than 2 meters. You must filter out the extreme values, or your car will get disaster.
	- 
- L298N & motor: This project controls the wheel speed by calculating how many cm per second of the car. Then calculate the time of motor running we need.

# Install opencv
`sudo apt-get install libopencv-dev`
`sudo apt-get install python3-opencv`
`sudo apt install -y python3-grpcio python3-grpc-tools`
`sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
`

