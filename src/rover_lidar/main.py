#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64MultiArray

class Zones():
    def __init__(self):
        self.pub = rospy.Publisher('LidarToPi', Float64MultiArray, queue_size=10)
        

    def publish(self):
        rospy.init_node('deez_nuts')
        arr = Float64MultiArray()
        arr.data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pub.publish(arr)
        print("Data recieved from lidar.")

    def stream(self):
        print("Running ros loop...")
        while not rospy.is_shutdown():
            rospy.Subscriber("scan", LaserScan, self.publish())
            rospy.sleep(1)


    


if __name__ == '__main__':
    zone = Zones()
    zone.stream()
