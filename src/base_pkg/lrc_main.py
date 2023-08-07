#!/usr/bin/env python3
from Communications import Communications
import rospy
from sensor_msgs.msg import Image

import sys
sys.path.append('../../../src/communications_lib')


print("Hi From Base Main Coms")
comPort1 = "/dev/ttyUSB0"
comPort2 = "/dev/ttyUSB0"
#commsOut = Communications(comPort1,pushTopic = 'RoverToBase', pullTopic = 'BaseToRover')
camOut = Communications(comPort2,pushTopic = 'BaseToCamera', pullTopic = 'CameraToBase', pushTopicType= Image)

# Initialize the Rover ROS_COMMS node
rospy.init_node('base_lrc', anonymous = True)
rate = rospy.Rate(10)  # Set the refresh rate (Hz)



if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    print("Hi From Base Main Coms")
    while not rospy.is_shutdown():

        # Send Data Out
        #commsOut.readData()
        
        camOut.readData()
        rate.sleep()

