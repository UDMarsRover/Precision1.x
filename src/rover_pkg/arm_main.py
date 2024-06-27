#!/usr/bin/env python3

import rospy
import time
from pyniryo2 import *
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Bool
from trajectory_msgs.msg import JointTrajectoryPoint
import sys
sys.path.append("..")
from src.UDMRT_datatypes import Arm_Position


class Arm:
    def __init__(self):
        rospy.init_node("arm", anonymous=True)
        self.reset()
        self.rate = rospy.Rate(10)

        self.currentPosition = Arm_Position()
        self.currentPosition.setState(self.robot.arm.get_pose().to_list())

        # self.robot.arm.move_pose([0.2, 0.1, 0.3, 0.0, 0.0, 0.0], callback=self.callback_pose())

        # publishers
        self.joint_pub = rospy.Publisher(
            "joint_pub", JointTrajectoryPoint, queue_size=10
        )
        self.pose_pub = rospy.Publisher("pose_pub", JointTrajectoryPoint, queue_size=10)

        # subscribers
        self.arm_sub = rospy.Subscriber(
            "arm/cmd/position", Float32MultiArray, self.callback_arm_command
        )

        self.grip_sub = rospy.Subscriber("grip_state", Bool, self.callback_grip_command)
        self.reset_sub = rospy.Subscriber("reset", Bool, self.callback_reset_command)

    def publish(self):
        # publish current pose values
        pose_array = JointTrajectoryPoint()
        pose = self.robot.arm.get_pose().to_list()
        pose_array.positions = pose
        self.pose_pub.publish(pose_array)

        # publish current joint values
        joint_array = JointTrajectoryPoint()
        joint = self.robot.arm.get_joints()
        joint_array.positions = joint
        self.joint_pub.publish(joint_array)

    # recieve command and move arm by specified value
    def callback_arm_command(self, msg):
        
        jog_values = msg.data

        self.currentPosition.updateState(jog_values)

        if jog_values != 0:
            print("Published ", self.currentPosition.getState())
            self.robot.arm.move_pose(self.currentPosition.getState(),callback=self.temp_callback)
        #print("Ran")

    def callback_grip_command(self, msg):
        if msg.data:
            self.robot.tool.grasp_with_tool()
            print("pressed")
        else:
            self.robot.tool.release_with_tool()

    def callback_reset_command(self, msg):
        if msg.data:
            self.robot.end()
            self.reset()

    def reset(self):
        # connect to arm
        robot_ip_address = "192.168.2.114"
        self.robot = NiryoRobot(robot_ip_address)

        
        self.robot.arm.calibrate_auto()  # calibrate motors
        self.robot.tool.update_tool()
        
        self.robot.arm.move_to_home_pose(callback=self.temp_callback)
        

    # def callback_pose(self):
    # print("current pose:",self.robot.arm.get_pose())

    def spin(self):
        rospy.spin()
        #arm.rate.sleep()
        print("spinning")

    def temp_callback(self,_):
        print("We ran this bitch")

arm = Arm()

print("Done Setting Up Arm")

while not rospy.is_shutdown():
    arm.spin()


print("super done")
arm.robot.end()  # disconnect from arm and ros
