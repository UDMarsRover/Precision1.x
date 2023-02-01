#!/usr/bin/env python3
import rospy

class Zones():
    def __init__(self):
        None

    def stream():
        None
        rospy.Subscriber("LaserScan", LaserScan, publish)
        self.pub = rospy.Publisher('LidarToPi', Int8MultiArray, queue_size=10)
        rospy.init_node('zone_shitter', anonymous=True)

    def publish():
        self.pub.publish([0, 0, 0, 0, 0, 0, 0, 0])

if __name__ == '__main__':
    zone = Zones()
    zone.stream
