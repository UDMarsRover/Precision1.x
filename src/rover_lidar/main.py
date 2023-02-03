#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32MultiArray

class Zones():
    def __init__(self):
        self.pub = rospy.Publisher('LidarToPi', Int32MultiArray, queue_size=10)
        

    def publish(self):
        rospy.init_node('deez_nuts')
        arr = Int32MultiArray()
        arr.data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(arr)
        print("Data recieved from lidar.")

    def stream(self):
        print("Running ros loop...")
        while not rospy.is_shutdown():
            rospy.Subscriber("scan", LaserScan, self.publish())
            rospy.sleep(10)


    


if __name__ == '__main__':
    zone = Zones()
    zone.stream()
