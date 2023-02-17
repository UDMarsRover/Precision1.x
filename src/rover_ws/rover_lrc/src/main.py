#!/usr/bin/env python3
from Communications import Communications
import rospy
from sensor_msgs.msg import Image


#comPort1 = "/dev/ttyUSB0"
comPort2 = "/dev/ttyUSB1"
#commsOut = Communications(comPort1,pushTopic = 'RoverToBase', pullTopic = 'BaseToRover')
camOut = Communications(comPort2,pushTopic = 'CameraToBase', pullTopic = 'BaseToCamera', pushTopicType= Image)

# Initialize the Rover ROS_COMMS node
rospy.init_node('rover_lrc', anonymous = True)
rate = rospy.Rate(10)               # Set the refresh rate



if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    while not rospy.is_shutdown():

        # Send Data Out
        #commsOut.readData()
        camOut.readData()
        rate.sleep()

