#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Bool
from std_msgs.msg import Float32
import time
import numpy as np
import sys
sys.path.append("..")
from src.UDMRT_datatypes import Arm_Position, LogitechF310


class udmrtController:
    def __init__(self):
        rospy.init_node("Controller_teleop", anonymous=True)
        self.drivePub = rospy.Publisher("motors/cmd/drive", Twist, queue_size=1)
        self.armPosPub = rospy.Publisher("arm/cmd/position", Float32MultiArray, queue_size=1)
        self.armMotorPub = rospy.Publisher("arm/cmd/motors", Float32MultiArray, queue_size=1)
        self.armGripPub = rospy.Publisher("arm/cmd/grip", Bool, queue_size=1)
        self.collectPub = rospy.Publisher("motors/cmd/collect", Twist, queue_size=1)
        self.camControl = rospy.Publisher("/pi/camera/servo", Float32, queue_size=1)

        self.rate = rospy.Rate(60)
        self.armRate = rospy.Rate(5)
        self.jog_pose_value = 0.02  # meters
        self.arm_jog_count = 0
        self.arm_reset_count = 0
        self.arm_cmd = Arm_Position()
        self.current_arm_command = Float32MultiArray()
        self.current_arm_command.data = (
            self.arm_cmd.getPosition()
        )  # command to update and publish
        self.current_arm_motor_command = Float32MultiArray()
        self.current_arm_motor_command.data = (
            self.arm_cmd.getMotors()
        )  # command to update and publish

        self.grip_command = False
        #self.armPosPub.publish(self.current_arm_command)
        #self.armGripPub.publish(self.grip_command)
        

        self.linVelY = 0
        self.angVelZ = 0
        self.collect1 = 0
        self.collect2 = 0
        self.collect3 = 0
        self.sec = time.time()
        self.velOut = Twist()
        self.camval = Float32()
        self.camval.data = 0.0
        self.velOut.linear.y = 0
        self.velOut.angular.z = 0
        self.velOut.angular.x = 0
        self.collectOut = Twist()
        self.collectOut.linear.x = 0
        self.collectOut.linear.y = 0
        self.collectOut.linear.z = 0
        self.drivePub.publish(self.velOut)
        self.current_start_state = 0

        self.controller = LogitechF310()

        print("Controller TeleOp Started Successfully!")

    def spin(self):
        motorRunning = self.__motor_command_check__()
        #self.__arm_command_check__()
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

        collect1_temp = self.controller.a
        collect2_temp = self.controller.b
        collect3_temp = self.controller.x
        cam_temp_l = self.controller.lt
        cam_temp_r = self.controller.rt

        self.camval.data =(-1 if self.controller.lt else 1 if self.controller.rt else 0) * 10
        self.camControl.publish(self.camval)

        print(self.camval.data)



        valueCheck = bool(
            (self.linVelY != linVelY_temp) or (angVelZ_temp != self.angVelZ) or (self.current_start_state)
        )

        collectCheck = bool (
            (self.collect1 != collect1_temp) or (self.collect2 !=collect2_temp) or (self.collect3 != collect3_temp)
        )

        
        self.linVelY = linVelY_temp
        self.angVelZ = angVelZ_temp

        self.collect1 = collect1_temp
        self.collect2 = collect2_temp
        self.collect3 = collect3_temp

        print(valueCheck)
        print(collectCheck)

        if collectCheck:
            self.collectOut.linear.x = -1.5 * float(self.controller.a)
            self.collectOut.linear.y = -1.5 * float(self.controller.b)
            self.collectOut.linear.z = 1.5 * float(self.controller.x)
            self.collectPub.publish(self.collectOut)
            
        else:
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
        #self.arm_cmd.roll = self.jog_pose_value * self.controller.rb  # roll
        #self.arm_cmd.roll += (
        #    self.jog_pose_value * self.controller.lb * -1
        #)  # negative roll

        #self.arm_cmd.pitch = self.jog_pose_value * self.controller.rt  # pitch
        #self.arm_cmd.pitch += (self.jog_pose_value * self.controller.lt * -1)  # negative pitch
        self.arm_cmd.yaw = self.jog_pose_value * self.controller.y  # yaw
        self.arm_cmd.yaw += self.jog_pose_value * self.controller.a * -1  # negative yaw

        if self.controller.rb and not self.controller.lb: self.arm_cmd.m0 = 1
        elif self.controller.lb and not self.controller.rb: self.arm_cmd.m0 = -1
        else: self.arm_cmd.m0 = 0


        self.grip_command = self.controller.b
        self.current_arm_command.data = self.arm_cmd.getPosition()
        self.current_arm_motor_command.data = self.arm_cmd.getMotors()

        if self.arm_cmd.nonZeroPosition():
            print("Publishing to Position:",self.current_arm_command)
            self.armPosPub.publish(self.current_arm_command)
        elif self.arm_cmd.nonZeroMotors():
            print("Publishing to Motors:",self.current_arm_motor_command)
            self.armMotorPub.publish(self.current_arm_motor_command)
        
        self.armGripPub.publish(self.grip_command)
        self.armRate.sleep()


controller = udmrtController()

while not rospy.is_shutdown():
    controller.spin()
