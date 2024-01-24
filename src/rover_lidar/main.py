#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray
import numpy as np

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)


def callback(msg):
    # Get an array of lengths in a specific zone
    # 1  0  7
    # 2     6
    # 3  4  5
    def getZone(i):
        lenr = len(msg.ranges)
        startidx = int(lenr / 16)        
        space = int(lenr / 8)
        starts = [0, startidx, startidx + space * 1, startidx + space * 2, startidx + space * 3,
             startidx + space * 4, startidx + space * 5, startidx + space * 6, startidx + space * 7]
        if i == 0:
            start1 = starts[8]
            end1 = lenr - 1
            print(start1, ", ", end1)
            start = starts[0]
            end = startidx
            left = msg.ranges[start1 : end1]
            right = msg.ranges[start : end]
            minLeft = min(left)
            minRight = min(right)
            return min(minLeft, minRight)
        else:
            start = starts[i]
            end = start + space
            return min(msg.ranges[start : end])


    def danger(i):
        j = getZone(i)
        j_prior = previous_ranges[i]
        # if j = inf and j_prior = 1, then j = 1
        if math.isinf(j) and j_prior < 4:
            return 0
        # if j = inf and j_prior = 4 then j = 4
        if math.isinf(msg.ranges[i]) and j_prior > 1:
            return 5
        if j < 0.20:
            return 1
        elif j < 0.50:
            return 2
        elif j < 2:
            return 3
        else:
            return 4

        
    previous_ranges = [0, 0, 0, 0, 0, 0, 0, 0]
    arr = Float32MultiArray()
    arr.data = [danger(0), danger(1), danger(2), danger(3), danger(4), danger(5), danger(6), danger(7)]
    previous_ranges = arr.data
    pub.publish(arr)
    print(previous_ranges)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
