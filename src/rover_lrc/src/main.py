#!/usr/bin/env python3
from communications import Communications
import rospy


comPort1 = "/dev/ttyUSB0"
comPort2 = ""
commsOut = Communications(comPort1,pushTopic = 'RoverToBase', pullTopic = 'BaseToRover', serialPort = comPort1)
camOut = Communications(comPort2,pushTopic = 'CameraToBase', pullTopic = 'BaseToCamera', serialPort = comPort2)

# Initialize the Rover ROS_COMMS node
rospy.init_node('rover_lrc', anonymous = True)
rate = rospy.Rate(10)               # Set the refresh rate



if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    while not rospy.is_shutdown():

        # Send Data Out
        commsOut.readData()
        camOut.readData()
        rate.sleep()

