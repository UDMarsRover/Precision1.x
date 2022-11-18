'''
Created By: Greg Molskow
Use Case:   To be used by the University of Dayton Mars Rover Team as a base class to define the sensors of the rover 
            and to interact with each of its parts. This code is approved for use only by UDMRT and its affiliates. 
'''

import rospy
import sys
from Communications import Communications
from std_msgs.msg import String

import UDMRTDataBuffer as DataBuf

class Rover:

    def __init__(self, commsPort, refreshRate =10):

        # Initialize the Rover data buffer
        self.dataBuf = DataBuf()

        # Initialize the Rover ROS_MAIN node
        rospy.init_node('rover_main', anonymous = True)
        rospy.rospy.Rate(refreshRate) #Hz

        # Initialize the Rover ROS Subscribers and tie them to the Data buffer
        rospy.Subscriber('EmoToPi', String, self.dataBuf.setEmoData)
        rospy.Subscriber('DriveToPi', String, self.dataBuf.setDriveMotorData)
        rospy.Subscriber('ArmToPi', String, self.dataBuf.setArmMotorData)
        rospy.Subscriber('BaseToRover', String, self.ingestBaseCommands)

        # Initalize Rover Comms Class
        self.comms = Communications('Rover',commsPort)



    def publishDataToRover(self):
        pub = rospy.Publisher('RoverToBase',String, queue_size = 10)
        rospy.rospy.Rate(10) #Hz
        command = self.dataBuf.composeMessageOut()
        rospy.loginfo("Buffer to Base:" + command)
        pub.publish(command)
        rate.sleep() #Not sure what this does, find out..

    def hasError(self):
        return self.dataBuf.checkForError()

    def getError(self):
        return self.dataBuf.getErrorMessageData()

    def ingestBaseCommands(self, dataIn):
        # Take in data from base and do things
        baseCommands = dataIn.data

        

#end