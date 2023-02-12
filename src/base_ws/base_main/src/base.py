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
        rospy.init_node('base_main', anonymous = True)
        rospy.rospy.Rate(refreshRate) #Hz

        rospy.Subscriber('CommsToBase', String, self.ingestRoverData)

    def publishDataToBase(self):
        pub = rospy.Publisher('BaseToRover',String, queue_size = 10)
        command = self.dataOutBuf.composeMessageOut()
        rospy.loginfo("Buffer to Base:" + command)
        pub.publish(command)

    def ingestRoverData(self, dataIn):
        # Take in data from rover and do things
        str = dataIn.data
        str = str.upper()
       
        pub = rospy.Publisher('BaseToGUI', String, queueSize = 10)
        
        self.dataIn.__errorMessageData__ = dataIn[0:1]
        self.dataIn.setDriveMotorData(dataIn.data[1:14])
        self.dataIn.setArmMotorData(dataIn.data[14:45])
        self.dataIn.setEmoEmoData(dataIn.data[45:86])

        pub.publish(self.dataIn.composeMessageOut())

        rospy.loginfo('Base to GUI: ' + self.dataIn.composeMessageOut())