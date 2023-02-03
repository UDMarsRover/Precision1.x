#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan

class Zones():
    def __init__(self):
        None

    def stream():
        rospy.Subscriber("scan", LaserScan, publish)
        self.pub = rospy.Publisher('LidarToPi', Int8MultiArray, queue_size=10)
        rospy.init_node('zone_shitter', anonymous=True)
        rospy.spin()


    def publish():
        self.pub.publish([0, 0, 0, 0, 0, 0, 0, 0])
        print("Data recieved from lidar.")


if __name__ == '__main__':
    zone = Zones()
    zone.stream
