#!/usr/bin/env python3
from communications import Communications
import rospy


comPort = "/dev/ttyUSB0"
commsOut = Communications('RoverComs',pushTopic = 'RoverToBase', pullTopic = 'BaseToRover', serialPort = comPort)
rate = rospy.Rate(10)               # Set the refresh rate


if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    while not rospy.is_shutdown():

        # Chech to see if data needs to be sent out
        commsOut.pushCheck()
        #ScommsOut.pullCheck()

        print("We Ran Yo")

        rate.sleep()

