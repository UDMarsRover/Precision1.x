import rospy
import sys
from std_msgs.msg import String

import UDMRTDataBuffer as DataBuf

class Base():

    def __init__(self, refreshRate =10):

        # Initialize the Base data buffer
        self.dataIn = DataBuf()
        self.dataOut = DataBuf()

        # Initialize the Base ROS_MAIN node
        rospy.init_node('rover_main', anonymous = True)
        rospy.rospy.Rate(refreshRate) #Hz

    def ingestRoverData(self, dataIn):
        # Take in data from rover and do things

        self.dataIn.__errorMessageData__ = dataIn[0:1]
        self.dataIn.setDriveMotorData(dataIn.data[1:14])
        self.dataIn.setArmMotorData(dataIn.data[14:45])
        self.dataIn.setEmoEmoData(dataIn.data[45:86])