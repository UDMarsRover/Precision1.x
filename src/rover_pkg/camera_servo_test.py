#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8

class CameraTester:
    def __init__(self):
        rospy.init_node("camera_servo_tester", anonymous=True)
        self.pub = rospy.Publisher("/base/gui/out/camera_servo", Int8, queue_size=10)
        self.rate = rospy.Rate(1)

    def run(self):
        while True:
            set_point = input("Enter motor setpoint as a value from 0 to 255: ")
            msg = Int8()
            msg.data = int(set_point)
            self.pub.publish(msg)
        

def main(args=None):
    ct = CameraTester()
    ct.run()


if __name__ == "__main__":
    main()