#!/usr/bin/env python3

import rospy
from inputs import get_gamepad
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import Bool

class ArmController():

    def __init__(self):    	
        rospy.init_node("arm_controller", anonymous=True)
        self.pub = rospy.Publisher('control_command', Float32MultiArray, queue_size=10)
        #self.pub_controller = rospy.Publisher('controller_state', Float32, queue_size=10)
        self.grip_pub = rospy.Publisher('grip_state', Bool, queue_size=10)
        self.reset_pub = rospy.Publisher('reset', Bool, queue_size=10)
        
        self.jog_pose_value = 0.02
        self.jog_count = 0 # count to update jog pose value
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.grip = False
        self.reset = False
        self.current_command = Float32MultiArray()
        self.current_command.data = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
        self.pub.publish(self.current_command)
        self.joint_state = JointTrajectoryPoint
        self.joint_sub = rospy.Subscriber('joint_pub', JointTrajectoryPoint, self.callback_joint_state)

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
        self.__update_command__()

        #self.__update_grip__()
        #self.grip_pub.publish(self.grip)
        self.__update_reset_command__()
        self.reset_pub.publish(self.reset)
        self.pub.publish(self.current_command)
        
     
    def callback_joint_state(self, msg):
        self.joint_state = msg.positions


    def __get_input__(self):

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
            self.count += 1 # update count

        return self.buttonBuffer
        
    def __update_command__(self):
        
        if self.count == 2: # 1 lt press gets registered as 2 
            self.jog_pose_value = 0.01
        elif self.count == 4:
            self.jog_pose_value = 0.005
        else:
            self.jog_pose_value = 0.02
            self.count = 0

        '''if joint_state[0] >= #rightmost threshold of base joint:
            self.x = jog_pose_value * float(self.buttonBuffer["dpad_x"])
            self.y = jog_pose_value * float(self.buttonBuffer["dpad_y"])
        elif joint_state[0] <= #leftmost threshold of base joint:
            self.x = jog_pose_value * float(self.buttonBuffer["dpad_x"] * -1)
            self.y = jog_pose_value * float(self.buttonBuffer["dpad_y"] * -1)
        else:
            self.x = self.jog_pose_value * float(self.buttonBuffer["dpad_y"] * -1)  # x
            self.y = self.jog_pose_value * float(self.buttonBuffer["dpad_x"] * -1) # y	'''        		
        self.z = self.jog_pose_value * float(self.buttonBuffer["y"]) # positive z
        self.z += self.jog_pose_value * float(self.buttonBuffer["a"] * -1) # negative z
        self.roll = self.jog_pose_value * float(self.buttonBuffer["rb"]) # roll
        self.pitch = self.jog_pose_value * float(self.buttonBuffer["lb"]) # pitch
        self.yaw = self.jog_pose_value * float(self.buttonBuffer["rt"]) # yaw
            
        self.current_command.data = [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
        
    def __update_grip__(self):
        self.grip = float(buttonBuffer["b"]) == 1
        
    def __update_reset_command__(self):
        self.reset = float(buttonBuffer["back"]) == 1
    		 

controller = ArmController()
while not rospy.is_shutdown():
	controller.spin()