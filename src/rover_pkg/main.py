#!/usr/bin/env python3
import rospy
import os
from rover import Rover as Presision1
import RPi.GPIO as gpio

# Create a rover instance
rate = 10  # Hz
p1 = Presision1(rate)
gpio.setmode(gpio.BCM)

indicatorLED = {"red": 22, "green": 27, "blue": 17}
shutdownPin = 4

gpio.setup(indicatorLED["red"], gpio.OUT)
gpio.setup(indicatorLED["green"], gpio.OUT)
gpio.setup(indicatorLED["blue"], gpio.OUT)
gpio.setup(shutdownPin, gpio.IN)


def led_control(r: int, g: int, b: int):
    gpio.output(indicatorLED["red"], r)
    gpio.output(indicatorLED["green"], g)
    gpio.output(indicatorLED["blue"], b)


def shutdown(check: bool = True):
    if check:
        if gpio.input(shutdownPin):
            os.system("systemctl poweroff")
            led_control(1, 1, 0)
    else:
        os.system("systemctl poweroff")
        led_control(1, 1, 0)


# The main Loop
if __name__ == "__main__":
    p1 = Rover()
    # Run when rover is not requested to die
    start = time.time()
    killCount = 0
    while not p1.kill:
        p1.spin()

        if not p1.wifiConnected:
            stop = Twist()
            stop.linear.y = 0
            stop.angular.z = 0
            drive.publish(stop)

    p1.log("Rover Killed")
    p1.led_control(0, 1, 1)
    print("KILLED")
    p1.shutdown()
