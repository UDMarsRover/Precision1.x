import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Bool
import time
import numpy as np
from inputs import get_gamepad
from UDMRT_datatypes import Arm_Position as arm_pos


class udmrtController:
    def __init__(self):
        rospy.init_node("Controller_teleop", anonymous=True)
        self.drivePub = rospy.Publisher("DriveVelocity", Twist, queue_size=1)
        self.armPosPub = rospy.Publisher("arm/cmd/position", Float32MultiArray, queue_size=1)
        self.armGripPub = rospy.Publisher("arm/cmd/grip", Bool, queue_size=1)
        self.rate = rospy.Rate(2)

        self.jog_pose_value = 0.02 # meters
        self.arm_cmd =arm_pos()
        self.current_arm_command = Float32MultiArray()
        self.current_arm_command.data = self.arm_cmd.getArmCommand() # command to update and publish


        self.linVelY = 0
        self.angVelZ = 0
        self.sec = time.time()
        self.velOut = Twist()
        self.velOut.linear.y = 0
        self.velOut.angular.z = 0
        self.velOut.angular.x = 0
        self.drivePub.publish(self.velOut)
        self.current_start_state = 0

        self.buttonBuffer = {
            "left_joy_y": 0,
            "left_joy_x": 0,
            "right_joy_y": 0,
            "right_joy_x": 0,
            "dpad_x": "",
            "dpad_y": "",
            "back": "",
            "start": "0",
            "a": "",
            "b": "",
            "x": "",
            "y": "",
            "rb": "",
            "lb": "",
            "rt": "",
            "lt": "",
        }

    def spin(self):
        self.__getInput__()
        motorRunning = self.__motor_command_check__()

    def __motor_command_check__(self):
        """
        This function checks to see if the controller is trying to send a command to the motors. If a command is trying to be sent, this function packages and sends the command over ROS. 

        :return: An indication if the motors have been commanded to run or not
        :rtype: bool
        """
        self.current_start_state = (
            self.buttonBuffer["start"]
            if self.buttonBuffer["start"] != self.current_start_state
            else 0
        )
        linVelY_temp = float(self.buttonBuffer["left_joy_y"])
        angVelZ_temp = float(self.buttonBuffer["left_joy_x"])

        linVelY_temp = linVelY_temp if np.abs(linVelY_temp) > 0.1 else 0
        angVelZ_temp = angVelZ_temp if np.abs(angVelZ_temp) > 0.1 else 0

        valueCheck = bool(
            (self.linVelY != linVelY_temp) or (angVelZ_temp != self.angVelZ)
        )
        self.linVelY = linVelY_temp
        self.angVelZ = angVelZ_temp

        #print(valueCheck)

        if valueCheck:
            self.velOut.linear.y = self.linVelY
            self.velOut.angular.z = self.angVelZ
            self.velOut.angular.x = float(self.current_start_state)
            self.drivePub.publish(self.velOut)
        
        return (self.velOut.linear.y != 0) and (self.velOut.angular.z != 0)

    def __arm_command_check__(self):

        if self.count == 2: # 1 lt press gets registered as 2 
            self.jog_pose_value = 0.01
        elif self.count == 4:
            self.jog_pose_value = 0.005
        else:
            self.jog_pose_value = 0.02
            self.count = 0

        self.arm_cmd.x = self.jog_pose_value * float(self.buttonBuffer["left_joy_y"])	
        self.arm_cmd.z = self.jog_pose_value * float(self.buttonBuffer["right_joy_y"]) # z
        self.arm_cmd.roll = self.jog_pose_value * float(self.buttonBuffer["rb"]) # roll
        self.arm_cmd.roll += self.jog_pose_value * float(self.buttonBuffer["lb"]) * -1 # negative roll
        self.arm_cmd.pitch = self.jog_pose_value * float(self.buttonBuffer["rt"]) # pitch
        self.arm_cmd.pitch += self.jog_pose_value * float(self.buttonBuffer["lt"]) * -1 # negative pitch
        self.arm_cmd.yaw = self.jog_pose_value * float(self.buttonBuffer["y"]) # yaw
        self.arm_cmd.yaw += self.jog_pose_value * float(self.buttonBuffer["a"]) * -1 # negative yaw
            
        self.current_arm_command.data = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]

    def __getInput__(self):
        """
        This function is used to take in the events from a Logitech controller and output them into a buffer for use.

        :param buttonBuffer: A buffer that will be sued to store the current state of the controller
        :type buttonBuffer: Required, List
        :return: An updated version of the buttonBuffer variable
        :rtype: List
        """

        event = get_gamepad()[0]
        if event.code == "BTN_THUMB":
            self.buttonBuffer["a"] = event.state
        elif event.code == "BTN_THUMB2":
            self.buttonBuffer["b"] = event.state
        elif event.code == "BTN_TRIGGER":
            self.buttonBuffer["x"] = event.state
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
            self.buttonBuffer["dpad_y"] = str(int(event.state) * -1)
        elif event.code == "BTN_BASE4":
            self.buttonBuffer["start"] = event.state
        elif event.code == "BTN_BASE3":
            self.buttonBuffer["back"] = event.state
        elif event.code == "BTN_PINKIE":
            self.buttonBuffer["rb"] = event.state
        elif event.code == "BTN_BASE2":
            self.buttonBuffer["rt"] = event.state
        elif event.code == "BTN_TOP2":
            self.buttonBuffer["lb"] = event.state
        elif event.code == "BTN_BASE":
            self.buttonBuffer["lt"] = event.state

        return self.buttonBuffer


controller = udmrtController()

while not rospy.is_shutdown():
    controller.spin()
