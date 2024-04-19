#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
import time

rospy.init_node("arm2", anonymous=True)

#event_state = Float32()
#prev_event_state = Float32()
command = Float32MultiArray()
        
#def callback_control_state(msg):
#	event_state.data = msg.data
	

def callback_arm_command(msg):
	command.data = msg.data
	
command_pub = rospy.Publisher('command', Float32MultiArray, queue_size=10)
#get_controller_sub = rospy.Subscriber('controller_state', Float32, callback_control_state)
get_command_sub = rospy.Subscriber('control_command', Float32MultiArray, callback_arm_command)





while not rospy.is_shutdown():
	#while prev_event_state.data == event_state.data:
	time.sleep(.2)
	command_pub.publish(command)
	
	#prev_event_state.data = event_state.data