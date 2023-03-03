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
        startidx = int(len(msg.ranges) / 16)
        print(startidx)
        starts = [0, 48, 143, 238, 333, 428, 523, 618]
        minval = 0
        increment = int(len(msg.ranges) / 16)
        print ("Length: ", len(msg.ranges))
        print("increment: ", increment)
        start = int(i * increment)
        stop = int((i + 2) * increment)
        if i > 0:
            arr = msg.ranges[start : stop]
            minval = min(arr)
        else:
            left = msg.ranges[0 : increment]
            right = msg.ranges[len(msg.ranges) - increment : len(msg.ranges) - 1]
            minleft = min(left)
            minright = min(right)
            minval = min(minleft, minright)

        

        return minval

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
