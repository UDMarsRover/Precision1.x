#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int8
import time
import RPi.GPIO as gpio

class CameraServoNode:
    def __init__(self):
        self.servo_pin = 11
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.servo_pin, gpio.OUT)
        self.p = gpio.PWM(self.servo_pin, 50)
        self.p.start(0) # duty cycle 2.5%
        rospy.init_node("camera_servo_node", anonymous=True)
        self.sub = rospy.Subscriber("/base/gui/out/camera_servo", Int8, self.callback)

    def callback(self, msg):
        print("Duty Cycle:" + str(msg.data))
        self.p.ChangeDutyCycle(msg.data)

    def stop(self):
        self.p.stop()
        gpio.cleanup()
        

def main(args=None):
        csn = CameraServoNode()
        try:
             rospy.spin()
        except:
             csn.stop()

if __name__ == "__main__":
    main()