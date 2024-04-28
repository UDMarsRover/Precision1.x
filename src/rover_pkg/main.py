#!/usr/bin/env python3
from std_msgs.msg import String
from geometry_msg.msg import Twist
from rover import Rover
import time
import rospy

drive = rospy.Publisher("DriveVelocity", Twist,queue_size=1)

# The main Loop
if __name__ == "__main__":
    p1 = Rover()
    # Run when rover is not requested to die
    start = time.time()
    killCount = 0
    while not p1.kill:
        p1.spin()
    
    if not p1.wifiConnected:
        stop = Twist()
        stop.linear.y = 0
        stop.angular.z = 0
        drive.publish(stop)
        
    p1.log("Rover Killed")
    p1.led_control(0,1,1)
    print("KILLED")
    p1.shutdown()
