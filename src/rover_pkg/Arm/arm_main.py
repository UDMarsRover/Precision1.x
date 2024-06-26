#!/usr/bin/env python3

import rospy
import time
from pyniryo2 import *
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Bool
from trajectory_msgs.msg import JointTrajectoryPoint


class Arm:
    def __init__(self):
        rospy.init_node("arm", anonymous=True)
        self.reset()

        # self.robot.arm.move_pose([0.2, 0.1, 0.3, 0.0, 0.0, 0.0], callback=self.callback_pose())

        # publishers
        self.joint_pub = rospy.Publisher(
            "joint_pub", JointTrajectoryPoint, queue_size=10
        )
        self.pose_pub = rospy.Publisher("pose_pub", JointTrajectoryPoint, queue_size=10)

        # subscribers
        self.arm_sub = rospy.Subscriber(
            "command", Float32MultiArray, self.callback_arm_command
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
        print("Published ", msg.data)
        self.robot.arm.jog_pose(msg.data)
        print("Ran")

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
        robot_ip_address = "10.10.10.10"
        self.robot = NiryoRobot(robot_ip_address)

        time.sleep(5)  # maybe helps more consistently start up

        self.robot.arm.calibrate_auto()  # calibrate motors
        self.robot.tool.update_tool()

        print("wait")
        time.sleep(1)
        print("done")
        self.robot.arm.move_to_home_pose()

    # def callback_pose(self):
    # print("current pose:",self.robot.arm.get_pose())


arm = Arm()
while not rospy.is_shutdown():
    while arm.robot.client.is_connected:
        arm.publish()  # continuously publish messages
    print("AHH CONNECTING")


print("super done")
arm.robot.end()  # disconnect from arm and ros
