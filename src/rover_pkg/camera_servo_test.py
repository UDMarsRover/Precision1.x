#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

class CameraTester:
    def __init__(self):
        rospy.init_node("camera_servo_tester", anonymous=True)
        self.pub = rospy.Publisher("/base/gui/out/camera_servo", Float32, queue_size=10)
        self.rate = rospy.Rate(1)

    def run(self):
        while True:
            set_point = input("Enter motor setpoint as a value from 0 to 255: ")
            msg = Float32()
            msg.data = float(set_point)
            self.pub.publish(msg)
            msg2 = Float32()
            msg2.data = 0.0
            self.pub.publish(msg2)
        

def main(args=None):
    ct = CameraTester()
    ct.run()


if __name__ == "__main__":
    main()