# https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library

# pip install adafruit-circuitpython-servokit
# pip install lgpio

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, address=0x41)


import time


kit.servo[0].set_pulse_width_range(300, 2500)
kit.servo[1].set_pulse_width_range(300, 2500)

# print(1)
# kit.servo[0].angle = 180
# time.sleep(1)

# print(2)
# kit.servo[0].angle = 0


for i in range(180):
    kit.servo[0].angle = i
    kit.servo[1].angle = i
    time.sleep(0.01)


for i in range(180)[::-1]:
    kit.servo[0].angle = i
    kit.servo[1].angle = i
    time.sleep(0.01)

kit.servo[0].angle = 15
kit.servo[1].angle = 15
