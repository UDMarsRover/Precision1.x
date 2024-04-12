#!/usr/bin/env python3

import rospy
from inputs import get_gamepad
from std_msgs.msg import Float32MultiArray


class ArmController():

    def __init__(self):    	
        rospy.init_node("arm_controller", anonymous=True)
        self.pub = rospy.Publisher('command', Float32MultiArray, queue_size=10)
        self.jog_pose_value = 0.02
        self.x = 0
        self.y = 0
        self.z = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.grip = False
        self.current_command = Float32MultiArray()
        self.current_command.data = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
        self.pub.publish(self.current_command)

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
	
    def spin(self):
        self.__get_input__()
        print("step1")
        self.__update_command__()
        print("step2")
        self.pub.publish(self.current_command)
        print("step3")


	
    def __get_input__(self):
        events = get_gamepad()
        for event in events:
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
                self.buttonBuffer["dpad_y"] = event.state
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
        
    def __update_command__(self):
        self.x = self.jog_pose_value * float(self.buttonBuffer["dpad_y"] * -1)  # x
        self.y = self.jog_pose_value * float(self.buttonBuffer["dpad_x"] * -1) # y
        self.z = self.jog_pose_value * float(self.buttonBuffer["y"]) # positive z
        self.z += self.jog_pose_value * float(self.buttonBuffer["a"] * -1) # negative z
        self.roll = self.jog_pose_value * float(self.buttonBuffer["rb"]) # roll
        self.pitch = self.jog_pose_value * float(self.buttonBuffer["lb"]) # pitch
        self.yaw = self.jog_pose_value * float(self.buttonBuffer["rt"]) # yaw
        
        self.current_command.data = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
     
    def __update_grip__(self):
    	if (float(buttonBuffer["b"]) == 1):
    		return True
  
controller = ArmController()
while not rospy.is_shutdown():
	controller.spin()
	print("spinning")	

 