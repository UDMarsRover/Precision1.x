'''
Created By: Greg Molskow
Use Case:   To be used by the University of Dayton Mars Rover Team as a base class to define the sensors of the rover 
            and to interact with each of its parts. This code is approved for use only by UDMRT and its affiliates. 
'''

import rospy
import sys
from std_msgs.msg import String

import UDMRTDataBuffer as DataBuf

class Rover:

    def __init__(self, refreshRate =10):

        # Initialize the Rover data buffer
        self.dataIn = DataBuf()
        self.dataOut = DataBuf()

        # Initialize the Rover ROS_MAIN node
        rospy.init_node('rover_main', anonymous = True)
        rospy.rospy.Rate(refreshRate) #Hz

        # Initialize the Rover ROS Subscribers and tie them to the Data buffer
        rospy.Subscriber('EmoToPi', String, self.dataOut.setEmoData)
            #Light on/off
        rospy.Subscriber('DriveToPi', String, self.dataOut.setDriveMotorData)
            #Speed left drive and speed right drive
        rospy.Subscriber('ArmToPi', String, self.dataOut.setArmMotorData)
            # 6 angles with ###.# presision
        rospy.Subscriber('BaseToRover', String, self.ingestBaseCommands)

        # Will be separate
        #rospy.Subscriber('CameraToBase', String, self.cameraIngest)
            





    def publishDataToBase(self):
        pub = rospy.Publisher('RoverToBase',String, queue_size = 10)
        rospy.rospy.Rate(10) #Hz
        command = self.dataOut.composeMessageOut()
        rospy.loginfo("Buffer to Base:" + command)
        pub.publish(command)
        rate.sleep() #Not sure what this does, find out..

    def hasError(self):
        return self.dataBuf.checkForError()

    def getError(self):
        return self.dataBuf.getErrorMessageData()

    def ingestBaseCommands(self, dataIn):
        # Take in data from base and do things

        self.dataIn.__errorMessageData__ = dataIn[0:1]
        self.dataIn.setDriveMotorData(dataIn.data[1:14])
        self.dataIn.setArmMotorData(dataIn.data[14:45])
        self.dataIn.setEmoEmoData(dataIn.data[45:86])




        

#end