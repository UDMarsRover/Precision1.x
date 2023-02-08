#!/usr/bin/env python3
import rospy
import numpy as np
from scipy import signal
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)

def callback(msg):
    # Get an array of lengths in a specific zone
    # 7  0  1
    # 6     2
    # 5  4  3
    def getZone(i):
        None
        dt = 0.001
        increment = len(msg.ranges) / 8
        start = int(i * increment)
        stop = int((i + 1) * increment)
        arr = msg.ranges[start : stop]
        
        return min(arr)

    print("Minimum in zone 0: " + str(getZone(0)))
    arr = Float32MultiArray()
    arr.data = [msg.ranges[360]]
    pub.publish(arr)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
