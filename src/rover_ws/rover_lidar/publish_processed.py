#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray
import numpy as np

pub = rospy.Publisher('Lidar_Processed', Float32MultiArray, queue_size=10)


def callback(msg):
    import numpy as np
    from scipy.ndimage import gaussian_filter

    # Assume your lidar scan array is stored in a variable called scan
    scan = np.array(msg.ranges) # 760 values representing the distances at angles

    # Apply a gaussian filter with a sigma value of your choice (e.g. 0.5)
    filtered_scan = gaussian_filter(scan, sigma=0.5)

    # Print or plot the filtered scan array
    print(filtered_scan)





rospy.init_node('processed_scan')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()