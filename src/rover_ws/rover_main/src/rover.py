'''
Created By: Greg Molskow
Use Case:   To be used by the University of Dayton Mars Rover Team as a base class to define the sensors of the rover 
            and to interact with each of its parts. This code is approved for use only by UDMRT and its affiliates. 
'''

import rospy
import sys
from std_msgs.msg import String

from UDMRTDataBuffer import UDMRTDataBuffer as DataBuf

class Rover:

    def __init__(self, refreshRate = 10):

        # Initialize the Rover data buffer
        self.dataInBuf = DataBuf()
        self.dataOutBuf = DataBuf()

        # Initialize the Rover ROS_MAIN node
        rospy.init_node('rover_main', anonymous = True)
        self.rate = rospy.rospy.Rate(refreshRate) #Hz

        # Initialize the Rover ROS Subscribers and tie them to the Data buffer
        rospy.Subscriber('EmoToPi', String, self.dataOutBuf.setEmoData)

        #Light on/off
        rospy.Subscriber('DriveToPi', String, self.dataOutBuf.setDriveMotorData)
            #Speed left drive and speed right drive
        rospy.Subscriber('ArmToPi', String, self.dataOutBuf.setArmMotorData)
            # 6 angles with ###.# presision
        rospy.Subscriber('BaseToRover', String, self.ingestBaseCommands)

        # Will be separate
        #rospy.Subscriber('CameraToBase', String, self.cameraIngest) 

    def publishDataToBase(self):
        pub = rospy.Publisher('RoverToBase',String, queue_size = 10)
        command = self.dataOutBuf.composeMessageOut()
        rospy.loginfo("Buffer to Base:" + command)
        pub.publish(command)

    def hasError(self):
        return self.dataBuf.checkForError()

    def getError(self):
        return self.dataBuf.getErrorMessageData()

    def ingestBaseCommands(self, dataIn):
        # Take in data from base and do things
        str = dataIn.data
        str = str.upper()

        #emoPub = rospy.Publisher('PiToEmo',String, queue_size = 10)
        drivePub = rospy.Publisher('PiToDrive',String, queue_size = 10)
        armPub = rospy.Publisher('PiToArm',String, queue_size = 10)

        self.dataInBuf.__errorMessageData__ = str[0:1]
        self.dataInBuf.setDriveMotorData(str[1:14])
        self.dataInBuf.setArmMotorData(str[14:45])
        self.dataInBuf.setEmoEmoData(str[45:86])

        #emoPub.publish(self.dataInBuf.getEmoData())
        drivePub.publish(self.dataInBuf.getDriveMotorData())
        armPub.publish(self.dataInBuf.getArmMotorData())

        #rospy.loginfo("Buffer to Emo:" + self.dataInBuf.getEmoData())
        rospy.loginfo("Buffer to Drive:" + self.dataInBuf.getDriveMotorData())
        rospy.loginfo("Buffer to Arm:" + self.dataInBuf.getArmMotorData())

        

        




        

#end