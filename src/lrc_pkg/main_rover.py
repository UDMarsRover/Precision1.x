#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from RFD900 import RFD900 as comms

comPort1 = "/dev/ttyUSB0"
resolution = [720,1280] #hight, width
#comPort2 = "/dev/ttyUSB1"
#commsOut = comms(comPort1)
camCom = comms(comPort1)

# Initialize the Rover ROS_COMMS node
rospy.init_node('rover_lrc', anonymous = True)

#comSub = rospy.Subscriber('RoverToBase', String,  commsOut.writeString)
#comPub = rospy.Publisher('BaseToRover', String, queue_size = 10)
camSub = rospy.Subscriber('CameraToBase', Image,  camCom.writeImage)
camPub = rospy.Publisher('BaseToCamera', Image, queue_size = 10)
rate = rospy.Rate(10)               # Set the refresh rate

camCom.openImageStream(resolution)

if (__name__ == '__main__'):
    # While roscore is up, running and connencted
    while not rospy.is_shutdown():

        # Get Incoming Data

        #data = commsOut.dataInBuffer

        # Write Outgoing Data
        #comPub.publish(data)

        #camCom.readImage()

        rate.sleep()

