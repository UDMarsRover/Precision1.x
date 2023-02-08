#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)

def callback(msg):
    # Get an array of lengths in a specific zone
    # 1  0  7
    # 2     6
    # 3  4  5
    def getZone(i):
        None
        dt = 0.001
        increment = len(msg.ranges) / 8
        start = int(i * increment)
        stop = int((i + 1) * increment)
        arr = msg.ranges[start : stop]
        n = 15  # the larger n is, the smoother curve will be
        b = [1.0 / n] * n
        a = 1
        smooth = lfilter(b, a, arr) * n

        return min(arr)

    def danger(i):
        j = getZone(i)
        if j < 0.20:
            return 1
        elif j < 0.50:
            return 2
        elif j < 2:
            return 3
        else: return 4
    
    print("Minimum in zone 7: " + str(getZone(7)))
    arr = Float32MultiArray()
    arr.data = [danger(0), danger(1), danger(2), danger(3), danger(4), danger(5), danger(6), danger(7)]
    pub.publish(arr)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
