#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
import time

rospy.init_node("arm2", anonymous=True)

command = Float32MultiArray()

# gets command data from controller input
def callback_arm_command(msg):
	command.data = msg.data
	
command_pub = rospy.Publisher('command', Float32MultiArray, queue_size=10)
get_command_sub = rospy.Subscriber('control_command', Float32MultiArray, callback_arm_command)

while not rospy.is_shutdown():
	time.sleep(.2) # slow down rate of publisher
	command_pub.publish(command) # continously publishes command data received from controller for 
								 # arm to receive