#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

class Zones():
    def __init__(self):
        self.pub = rospy.Publisher('LidarToPi', Float32MultiArray, queue_size=10)
        
    

    def stream(self):
        def callback(msg):
            print("BRUH")
            rospy.init_node('deez_nuts')
            arr = Float32MultiArray()
            print(msg.ranges[0])
            # arr.data = [LaserScan.ranges[0], 0, 0, 0, 0, 0, 0, 0]
            # self.pub.publish(arr)

        print("Running ros loop...")
        while not rospy.is_shutdown():
            print("Data recieved from lidar.")
            self.sub = rospy.Subscriber("scan", LaserScan, callback)
            rospy.sleep(1)


    


if __name__ == '__main__':
    zone = Zones()
    zone.stream()
