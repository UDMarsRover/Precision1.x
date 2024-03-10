#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan 

def callback(data):
    print(data.ranges[0])

def do_shit():
    # Initialize a node for this script
    rospy.init_node("lidar_gui_node", anonymous=True)
    sub = rospy.Subscriber("scan", LaserScan, callback)
    rospy.spin()

if __name__ == "__main__":
    try:
        do_shit()
    except rospy.ROSInterruptException:
        pass
