#!/usr/bin/env python3

import rospy
from inputs import get_gamepad
from std_msgs.msg import Float32MultiArray
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import Bool


class ArmController:
    def __init__(self):
        rospy.init_node("arm_controller", anonymous=True)
        # publishers
        self.pub = rospy.Publisher(
            "control_command", Float32MultiArray, queue_size=10
        )  # publish jog pose command
        self.grip_pub = rospy.Publisher("grip_state", Bool, queue_size=10)
        self.reset_pub = rospy.Publisher(
            "reset", Bool, queue_size=10
        )  # publish command to move to home pose

        self.reset_count = 0
        # initialize publish values
        self.jog_pose_value = 0.02  # meters
        self.count = 0  # count to update jog pose value
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.grip = False
        self.reset = False
        self.joint_state = [0]
        self.current_command = Float32MultiArray()
        self.current_command.data = [
            self.x,
            self.y,
            self.z,
            self.roll,
            self.pitch,
            self.yaw,
        ]  # command to update and publish

        self.pub.publish(self.current_command)  # publish first command (all zeros)

        # subscriber to receive joint state
        self.joint_sub = rospy.Subscriber(
            "joint_pub", JointTrajectoryPoint, self.callback_joint_state
        )

        # inputs for controller
        self.buttonBuffer = {
            "left_joy_y": 0,
            "left_joy_x": 0,
            "right_joy_y": 0,
            "right_joy_x": 0,
            "dpad_x": 0,
            "dpad_y": 0,
            "back": 0,
            "start": 0,
            "a": 0,
            "b": 0,
            "x": 0,
            "y": 0,
            "rb": 0,
            "lb": 0,
            "rt": 0,
            "lt": 0,
        }

    # call each function and publish
    def spin(self):
        self.__get_input__()
        self.__update_command__()

        self.__update_grip__()
        self.grip_pub.publish(self.grip)
        self.__update_reset_command__()
        if self.reset_count == 2:
            self.reset_pub.publish(True)  # publish command to move to home pose
            self.reset_count = 0
        else:
            self.reset_pub.publish(False)
        self.pub.publish(self.current_command)

    # sets current joint state from message
    def callback_joint_state(self, msg):
        self.joint_state = msg.positions

    # get controller input
    # registers 2 presses, only updates when input is changed (can't be held)
    def __get_input__(self):
        event = get_gamepad()[0]
        if event.code == "BTN_THUMB":
            self.buttonBuffer["a"] = event.state
        elif event.code == "BTN_THUMB2":
            self.buttonBuffer["b"] = event.state
        elif event.code == "BTN_TRIGGER":
            self.buttonBuffer["x"] = event.state
            self.count += 1  # update count
        elif event.code == "BTN_TOP":
            self.buttonBuffer["y"] = event.state
        elif event.code == "ABS_Y":
            self.buttonBuffer[
                "left_joy_y"
            ] = f"{round((int(event.state) - 128)/-128,1)}"
        elif event.code == "ABS_X":
            self.buttonBuffer["left_joy_x"] = f"{round((int(event.state) - 128)/128,1)}"
        elif event.code == "ABS_RZ":
            self.buttonBuffer[
                "right_joy_y"
            ] = f"{round((int(event.state) - 128)/-128,1)}"
        elif event.code == "ABS_Z":
            self.buttonBuffer[
                "right_joy_x"
            ] = f"{round((int(event.state) - 128)/128,1)}"
        elif event.code == "ABS_HAT0X":
            self.buttonBuffer["dpad_x"] = event.state
        elif event.code == "ABS_HAT0Y":
            self.buttonBuffer["dpad_y"] = event.state
        elif event.code == "BTN_BASE4":
            self.buttonBuffer["start"] = event.state
        elif event.code == "BTN_BASE3":
            self.buttonBuffer["back"] = event.state
            self.reset_count += 1
        elif event.code == "BTN_PINKIE":
            self.buttonBuffer["rb"] = event.state
        elif event.code == "BTN_BASE2":
            self.buttonBuffer["rt"] = event.state
        elif event.code == "BTN_TOP2":
            self.buttonBuffer["lb"] = event.state
        elif event.code == "BTN_BASE":
            self.buttonBuffer["lt"] = event.state

        return self.buttonBuffer

    def __update_command__(self):
        if self.count == 2:  # 1 lt press gets registered as 2
            self.jog_pose_value = 0.01
        elif self.count == 4:
            self.jog_pose_value = 0.005
        else:
            self.jog_pose_value = 0.02
            self.count = 0

        self.y = self.jog_pose_value * float(self.buttonBuffer["left_joy_x"]) * -1

        if self.joint_state[0] <= -0.9 and self.y < 0:
            self.y = 0
        if self.joint_state[0] >= 0.9 and self.y > 0:
            self.y = 0

        """if self.joint_state[0] >= 0.9: #rightmost threshold of base joint:
            self.x = self.jog_pose_value * float(self.buttonBuffer["left_joy_x"]) * -1
            self.y = self.jog_pose_value * float(self.buttonBuffer["left_joy_y"]) * -1
        elif self.joint_state[0] >= 0.9: #leftmost threshold of base joint:
            self.x = self.jog_pose_value * float(self.buttonBuffer["left_joy_x"])
            self.y = self.jog_pose_value * float(self.buttonBuffer["left_joy_y"])
        else:
            self.x = self.jog_pose_value * float(self.buttonBuffer["left_joy_y"])
            self.y = self.jog_pose_value * float(self.buttonBuffer["left_joy_x"]) * -1	"""

        self.x = self.jog_pose_value * float(self.buttonBuffer["left_joy_y"])
        # self.y = self.jog_pose_value * float(self.buttonBuffer["left_joy_x"]) * -1
        self.z = self.jog_pose_value * float(self.buttonBuffer["right_joy_y"])  # z
        self.roll = self.jog_pose_value * float(self.buttonBuffer["rb"])  # roll
        self.roll += (
            self.jog_pose_value * float(self.buttonBuffer["lb"]) * -1
        )  # negative roll
        self.pitch = self.jog_pose_value * float(self.buttonBuffer["rt"])  # pitch
        self.pitch += (
            self.jog_pose_value * float(self.buttonBuffer["lt"]) * -1
        )  # negative pitch
        self.yaw = self.jog_pose_value * float(self.buttonBuffer["y"])  # yaw
        self.yaw += (
            self.jog_pose_value * float(self.buttonBuffer["a"]) * -1
        )  # negative yaw

        self.current_command.data = [
            self.x,
            self.y,
            self.z,
            self.roll,
            self.pitch,
            self.yaw,
        ]

    def __update_grip__(self):
        self.grip = float(self.buttonBuffer["b"]) == 1

    # def __update_reset_command__(self):
    #   self.reset = float(self.buttonBuffer["back"]) == 1


controller = ArmController()
while not rospy.is_shutdown():
    controller.spin()  # continously run class functions
