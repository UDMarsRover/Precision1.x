import time
import rospy
import sys
from std_msgs.msg import String
from communications import Communications
import rover as Presision1

# Define the port fro the USB antenna 
comPort = "/dev/ttyUSB0"

# Create a rover instance
p1 = Presision1()






# The main Loop
if __name__ == '__main__':

    # While roscore is running
    while not rospy.is_shutdown():

        if (p1.hasError()):
            print(" i seem to has an ewwow :( plz hewp me :,(...."+p1.getError())

        print("Main loop yo")

        rospy.spin()

    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
