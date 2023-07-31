#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from RFD900 import RFD900 as comms

comPort1 = "/dev/ttyUSB0"
resolution = [240,320] #hight, width
#comPort2 = "/dev/ttyUSB1"
#commsOut = Communications(comPort1,pushTopic = 'RoverToBase', pullTopic = 'BaseToRover')
#camOut = Communications(comPort2,pushTopic = 'CameraToBase', pullTopic = 'BaseToCamera', pushTopicType= Image)
camCom = comms(comPort1)

# Initialize the Rover ROS_COMMS node
rospy.init_node('rover_lrc', anonymous = True)
rospy.Subscriber('CameraToBase', Image,  camCom.readImage)
rate = rospy.Rate(10)               # Set the refresh rate

camCom.openImageStream(resolution)

if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    while not rospy.is_shutdown():

        # Send Data Out
        #commsOut.readData()
        camCom.readImage()

        rate.sleep()

