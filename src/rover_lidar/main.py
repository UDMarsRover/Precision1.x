#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)
def callback(msg):
    arr = Float32MultiArray()
    arr.data = [msg.ranges[0]]
    print("Number of values in ranges" + str(len(msg.ranges)))
    print("Minimum angle: " + str(msg.angle_min))
    print("Maximum angle: " + str(msg.angle_max))
    print("Angle increment" + str(msg.angle_increment))
    pub.publish(arr)



rospy.init_node('scan_values')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()
