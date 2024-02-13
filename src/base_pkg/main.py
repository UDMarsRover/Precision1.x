#!/usr/bin/env python3
import time
import rospy
import sys
from std_msgs.msg import String
from base import Base as Precision1Base

# Create a rover instance
rate = 10 #Hz
p1b = Precision1Base(rate)

# The main Loop
if __name__ == '__main__':

    # While roscore is running
    while not rospy.is_shutdown():

        if (p1b.hasError()):
            print(" i seem to has an ewwow :( plz hewp me :,(...."+p1b.getError())
        else:
            p1b.publishDataToBase()

        # Sleep for a set amount of time to keep our rate
        p1b.rate.sleep()

    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
