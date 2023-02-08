#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)
def callback(msg):
    arr = Float32MultiArray()
    arr.data = [msg.ranges[0]]
    print("Minimum angle: " + str(msg.range_min))
    print("Maximum angle: " + str(msg.range_max))
    pub.publish(arr)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
