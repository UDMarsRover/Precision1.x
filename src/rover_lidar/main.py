#!/usr/bin/env python3
import rospy
import numpy as np
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
        n = len(arr)
        fhat = np.fft.fft(arr, n)
        psd = fhat * np.conj(fhat)/n
        freq = (1/(dt*n)) * np.arange(n)
        idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index

        ## Filter out noise
        threshold = 100
        psd_idxs = psd > threshold #array of 0 and 1
        psd_clean = psd * psd_idxs #zero out all the unnecessary powers
        fhat_clean = psd_idxs * fhat #used to retrieve the signal

        signal_filtered = np.fft.ifft(fhat_clean) #inverse fourier transform
        return min(signal_filtered)

    print("Minimum in zone 0: " + str(getZone(0)))
    arr = Float32MultiArray()
    arr.data = [msg.ranges[360]]
    pub.publish(arr)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
