#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray
import numpy

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)

def callback(msg):
    # Get an array of lengths in a specific zone
    # 1  0  7
    # 2     6
    # 3  4  5
    def getZone(i):
        min = 0
        increment = int(len(msg.ranges) / 16)
        start = int(i * increment)
        stop = int((i + 2) * increment)
        if i > 0:
            arr = msg.ranges[start : stop]
            min = min(arr)
        else:
            None
            left = np.array(msg.ranges[0 : increment])
            right = np.array(msg.ranges[len(msg.ranges) - increment : len(msg.ranges) - 1])
            min = min(np.minimum(left, right))

        # increment = int(len(msg.ranges) / 16)
        # start = int(i * increment)
        # stop = int((i + 2) * increment)
        # arr = msg.ranges[start : stop]
        # if (i == 0): 
        #     start1 = int(len(msg.ranges) - increment)
        #     end1 = int(len(msg.ranges) - 1)
        #     start2 = int(0)
        #     end2 = increment
        #     arr = numpy.concatenate(msg.ranges[start1 : end1], msg.ranges[start2 : end2])
        #     arr = msg.ranges[start1 : end1]

        

        return min(arr)

    def danger(i):
        j = getZone(i)
        j_prior = previous_ranges[i]
        # if j = inf and j_prior = 1, then j = 1
        if math.isinf(msg.ranges[i]) and j_prior < 4:
            print("SO CLOSE")
            return 1
        # if j = inf and j_prior = 4 then j = 4
        if math.isinf(msg.ranges[i]) and j_prior > 1:
            print("SO FAR")
            return 4
        if j < 0.20:
            j = 1
        elif j < 0.50:
            j = 2
        elif j < 2:
            j = 3
        else:
            j = 4

        return j
        
    previous_ranges = [0, 0, 0, 0, 0, 0, 0, 0]
    arr = Float32MultiArray()
    arr.data = [danger(0), danger(1), danger(2), danger(3), danger(4), danger(5), danger(6), danger(7)]
    previous_ranges = arr.data
    pub.publish(arr)
    print(previous_ranges)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
