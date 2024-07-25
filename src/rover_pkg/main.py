#!/usr/bin/env python3
import rospy
import os
from rover import Rover as Presision1
import RPi.GPIO as gpio

# Create a rover instance
rate = 10  # Hz
p1 = Presision1(rate)



# The main Loop
if __name__ == "__main__":
    # Run when rover is not requested to die
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
