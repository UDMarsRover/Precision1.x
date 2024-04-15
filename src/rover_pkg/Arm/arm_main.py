#!/usr/bin/env python3

import rospy
import time
from pyniryo2 import *
from std_msgs.msg import Float32MultiArray
#from std_msgs.msg import Bool
from trajectory_msgs.msg import JointTrajectoryPoint
#from niryo_listener import ArmController


class Arm():

	def __init__(self):
		rospy.init_node("arm",anonymous = True)
		robot_ip_address = "10.10.10.10"
		self.robot = NiryoRobot(robot_ip_address)
		time.sleep(5)
		self.robot.arm.calibrate_auto()
		#self.robot.tool.update_tool()
		print("wait")
		time.sleep(1)
		print("done")
		self.robot.arm.move_to_home_pose()

		self.pose_pub = rospy.Publisher('pose_pub', JointTrajectoryPoint, queue_size=10)
		#self.command_pub = rospy.Publisher('command', Float32MultiArray, queue_size=10)
		self.arm_sub = rospy.Subscriber('command', Float32MultiArray, self.callback_arm_command)
		#self.grip_sub = rospy.Subscriber('grip_state', Bool, self.callback_grip_command)
	    
	def publish(self):
	    
		pose_array = JointTrajectoryPoint()
		pose = self.robot.arm.get_pose().to_list()
		pose_array.positions = pose
		self.pose_pub.publish(pose_array)

		#command = Float32MultiArray()
		#command.data = [0.01, 0, 0, 0, 0, 0]
		#self.command_pub.publish(command)
	    	
	def callback_arm_command(self, msg):
		print("Published ",msg.data)
		self.robot.arm.jog_pose(msg.data)
		
	'''def callback_grip_command(self, msg):
		if(msg):
			self.robot.tool.grasp_with_tool()
		else:
			self.robot.tool.release_with_tool()'''


		


arm = Arm()
#controller = ArmController()
#rate = rospy.Rate(10)
while not rospy.is_shutdown():

    #controller.spin()
    arm.publish() 
    while not arm.robot.client.is_connected: print("AHH CONNECTING")
    #rate.sleep()
          
print("super done")  
arm.robot.end()

