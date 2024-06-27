#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Bool
import time
import numpy as np
import sys
sys.path.append("..")
from src.UDMRT_datatypes import Arm_Position, LogitechF310


class udmrtController:
    def __init__(self):
        rospy.init_node("Controller_teleop", anonymous=True)
        self.drivePub = rospy.Publisher("DriveVelocity", Twist, queue_size=1)
        self.armPosPub = rospy.Publisher(
            "arm/cmd/position", Float32MultiArray, queue_size=1
        )
        self.armGripPub = rospy.Publisher("arm/cmd/grip", Bool, queue_size=1)
        self.rate = rospy.Rate(60)

        self.jog_pose_value = 0.02  # meters
        self.arm_jog_count = 0
        self.arm_reset_count = 0
        self.arm_cmd = Arm_Position()
        self.current_arm_command = Float32MultiArray()
        self.current_arm_command.data = (
            self.arm_cmd.getState()
        )  # command to update and publish
        self.grip_command = False
        self.armPosPub.publish(self.current_arm_command)
        self.armGripPub.publish(self.grip_command)
        

        self.linVelY = 0
        self.angVelZ = 0
        self.sec = time.time()
        self.velOut = Twist()
        self.velOut.linear.y = 0
        self.velOut.angular.z = 0
        self.velOut.angular.x = 0
        self.drivePub.publish(self.velOut)
        self.current_start_state = 0

        self.controller = LogitechF310()

        print("Controller TeleOp Started Successfully!")

    def spin(self):
        #motorRunning = self.__motor_command_check__()
        self.__arm_command_check__()
        self.rate.sleep()

    def __motor_command_check__(self):
        """
        This function checks to see if the controller is trying to send a command to the motors. If a command is trying to be sent, this function packages and sends the command over ROS.

        :return: An indication if the motors have been commanded to run or not
        :rtype: bool
        """
        self.current_start_state = (
            self.controller.start
            if self.controller.start != self.current_start_state
            else 0
        )
        linVelY_temp = self.controller.left_joy_y
        angVelZ_temp = self.controller.left_joy_x

        linVelY_temp = linVelY_temp if np.abs(linVelY_temp) > 0.1 else 0
        angVelZ_temp = angVelZ_temp if np.abs(angVelZ_temp) > 0.1 else 0

        valueCheck = bool(
            (self.linVelY != linVelY_temp) or (angVelZ_temp != self.angVelZ)
        )
        self.linVelY = linVelY_temp
        self.angVelZ = angVelZ_temp

        # print(valueCheck)

        if valueCheck:
            self.velOut.linear.y = self.linVelY
            self.velOut.angular.z = self.angVelZ
            self.velOut.angular.x = self.current_start_state
            self.drivePub.publish(self.velOut)

        return (self.velOut.linear.y != 0) and (self.velOut.angular.z != 0)

    def __arm_command_check__(self):

        if self.controller.x: self.arm_jog_count += 1

        if self.arm_jog_count == 2:  # 1 lt press gets registered as 2
            self.jog_pose_value = 0.01
        elif self.arm_jog_count == 4:
            self.jog_pose_value = 0.005
        else:
            self.jog_pose_value = 0.02
            self.arm_jog_count = 0

        self.arm_cmd.x = self.jog_pose_value * self.controller.left_joy_y
        self.arm_cmd.y = self.jog_pose_value * self.controller.left_joy_x
        self.arm_cmd.z = self.jog_pose_value * self.controller.right_joy_y  # z
        self.arm_cmd.roll = self.jog_pose_value * self.controller.rb  # roll
        self.arm_cmd.roll += (
            self.jog_pose_value * self.controller.lb * -1
        )  # negative roll
        self.arm_cmd.pitch = self.jog_pose_value * self.controller.rt  # pitch
        self.arm_cmd.pitch += (
            self.jog_pose_value * self.controller.lt * -1
        )  # negative pitch
        self.arm_cmd.yaw = self.jog_pose_value * self.controller.y  # yaw
        self.arm_cmd.yaw += self.jog_pose_value * self.controller.a * -1  # negative yaw

        self.grip_command = self.controller.b
        self.current_arm_command.data = self.arm_cmd.getState()

        if self.arm_cmd.nonZeros():
            self.armPosPub.publish(self.current_arm_command)
            self.armGripPub.publish(self.grip_command)


controller = udmrtController()

while not rospy.is_shutdown():
    controller.spin()
