
import rospy
from geometry_msgs.msg import Twist
import time
import numpy as np

rospy.init_node("Controller_teleop", anonymous=True)
pub = rospy.Publisher("DriveVelocity", Twist, queue_size=10)

rate = rospy.Rate(5)


buttonBuffer = {
        "left_joy_y"  :0,
        "left_joy_x"  :0,
        "right_joy_y" :0,
        "right_joy_x" :0,
        "dpad_x":"",
        "dpad_y":"",
        "back":"",
        "start":"0",
        "a":"",
        "b":"",
        "x":"",
        "y":"",
        "rb":"",
        "lb":"",
        "rt":"",
        "lt":""
    }

def controllerMap(buttonBuffer:list):
    from inputs import get_gamepad

    event = get_gamepad()[0]
    if      event.code == "BTN_THUMB"   : buttonBuffer["a"] = event.state
    elif    event.code == "BTN_THUMB2"  : buttonBuffer["b"] = event.state
    elif    event.code == "BTN_TRIGGER" : buttonBuffer["x"] = event.state
    elif    event.code == "BTN_TOP"     : buttonBuffer["y"] = event.state
    elif    event.code == "ABS_Y"       : buttonBuffer["left_joy_y"] = f"{round((int(event.state) - 128)/-128,1)}"
    elif    event.code == "ABS_X"       : buttonBuffer["left_joy_x"] = f"{round((int(event.state) - 128)/128,1)}"
    elif    event.code == "ABS_RZ"      : buttonBuffer["right_joy_y"] = f"{round((int(event.state) - 128)/-128,1)}"
    elif    event.code == "ABS_Z"       : buttonBuffer["right_joy_x"] = f"{round((int(event.state) - 128)/128,1)}"
    elif    event.code == "ABS_HAT0X"   : buttonBuffer["dpad_x"] = event.state
    elif    event.code == "ABS_HAT0Y"   : buttonBuffer["dpad_y"] = str(int(event.state) * -1)
    elif    event.code == "BTN_BASE4"   : buttonBuffer["start"] = event.state
    elif    event.code == "BTN_BASE3"   : buttonBuffer["back"] = event.state
    elif    event.code == "BTN_PINKIE"  : buttonBuffer["rb"] = event.state
    elif    event.code == "BTN_BASE2"   : buttonBuffer["rt"] = event.state
    elif    event.code == "BTN_TOP2"    : buttonBuffer["lb"] = event.state
    elif    event.code == "BTN_BASE"    : buttonBuffer["lt"] = event.state
    
    return buttonBuffer

linVelY = 0
angVelZ = 0
sec = time.time()
velOut = Twist()
velOut.linear.y = 0
velOut.angular.z = 0
pub.publish(velOut)
current_start_state = 0


while not rospy.is_shutdown() :
    controllerMap(buttonBuffer)
    current_start_state = buttonBuffer["start"] if buttonBuffer["start"] != current_start_state else 0
    linVelY_temp = float(buttonBuffer["left_joy_y"])
    angVelZ_temp = float(buttonBuffer["left_joy_x"])
    if ((time.time()-sec > 0.1) or
        (np.abs(angVelZ_temp) <= 0.1) or
        (np.abs(linVelY_temp) <= 0.1)):

        if ((np.abs(linVelY_temp) >= np.abs(linVelY) + 0.2) or 
            (np.abs(linVelY_temp) <= np.abs(linVelY) - 0.2) or
            (np.abs(angVelZ_temp) >= np.abs(angVelZ) + 0.2) or
            (np.abs(angVelZ_temp) <= np.abs(angVelZ) - 0.2)):

            linVelY = linVelY_temp if np.abs(linVelY_temp) > 0.1 else 0
            angVelZ = angVelZ_temp if np.abs(angVelZ_temp) > 0.1 else 0
            print(linVelY,angVelZ)

            
            velOut.linear.y = linVelY
            velOut.angular.z = angVelZ
            velOut.angular.x = float(current_start_state)
            pub.publish(velOut)
        sec = time.time()