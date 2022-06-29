#!/usr/bin/env python3
import time
import rospy
import sys
from std_msgs.msg import String as rosstring
from communications import Communications

pushTopic = 'RoverToBase'
count = 0
pub = rospy.Publisher(pushTopic, rosstring, queue_size=1)
rospy.init_node('RoverMain')

comPort = "/dev/ttyUSB0"
comms = Communications('RoverComs', serialPort = comPort)
rate = rospy.Rate(10)               # Set the refresh rate


if __name__ == '__main__':
    while not rospy.is_shutdown():
        #Check the comms topic for any ingoing or outgoing message.
        
        print("Data")
        dataIn = comms.readData()
        print(dataIn)
        if comms.error != None :
            print("execption founds")
            print(comms.error)
            sys.exit()

        comms.DataOutBuffer = comms.DataInBuffer

        comms.writeData()
        if comms.error != None :
            print("execption found")
            print(comms.error)
            sys.exit()
    




