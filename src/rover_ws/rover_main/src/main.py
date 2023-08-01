#!/usr/bin/env python3
import time
import rospy
import sys
from std_msgs.msg import String
from rover import Rover as Presision1

# Create a rover instance
rate = 10 #Hz
p1 = Presision1(rate)

# The main Loop
if __name__ == '__main__':

    # While roscore is running
    while not rospy.is_shutdown():

        if (p1.hasError()):
            print(" i seem to has an ewwow :( plz hewp me :,(...."+p1.getError())
        else:
            p1.publishDataToBase()

        # Sleep for a set amount of time to keep our rate
        p1.rate.sleep()

    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
