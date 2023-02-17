#!/usr/bin/env python3
import rospy
import sys
from std_msgs.msg import String

from UDMRTDataBuffer import UDMRTDataBuffer as DataBuf

class Base():

    def __init__(self, refreshRate =10):

        # Initialize the Base data buffer
        self.dataInBuf = DataBuf()
        self.dataOutBuf = DataBuf()

        # Initialize the Base ROS_MAIN node
        rospy.init_node('base_main', anonymous = True)
        self.rate = rospy.Rate(refreshRate) #Hz

        rospy.Subscriber('CommsToBase', String, self.ingestRoverData)

    def publishDataToBase(self):
        pub = rospy.Publisher('BaseToRover',String, queue_size = 10)
        command = self.dataOutBuf.composeMessageOut()
        rospy.loginfo("Buffer to Base:" + command)
        pub.publish(command)

    def hasError(self):
        return self.dataInBuf.checkForError()

    def ingestRoverData(self, dataIn):
        # Take in data from rover and do things
        str = dataIn.data
        str = str.upper()
       
        pub = rospy.Publisher('BaseToGUI', String, queueSize = 10)
        
        self.dataInBuf.__errorMessageData__ = dataIn[0:1]
        self.dataInBuf.setDriveMotorData(dataIn.data[1:14])
        self.dataInBuf.setArmMotorData(dataIn.data[14:45])
        self.dataInBuf.setEmoData(dataIn.data[45:86])

        pub.publish(self.dataInBuf.composeMessageOut())

        rospy.loginfo('Base to GUI: ' + self.dataInBuf.composeMessageOut())