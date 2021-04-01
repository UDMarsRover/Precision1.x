# This node will be used to control the drive motors

import rospy
from std_msgs.msg import String




# this function handles input from the control device
def takeInCommnad(dataIn):
    motors = rospy.Publisher('driverToMotors',String, queue_size = 10)
    rospy.rospy.Rate(10) #Hz
    commandIn = dataIn.data
    rospy.loginfo(commandIn)
    pub.publish(commandIn)
    rate.sleep() #Not sure what this does, find out..
    
def takeInMotorData(dataIn)
    rospy.loginfo(dataIn.data) #for now, just log Arduino responce


if __name__ == '__main__':
    rospy.Subscriber('controlToDriver', String, takeInCommnad)
    rospy.Subscriber('motorsToDriver', String, takeInMotorData)
    rospy.init_node('driver', anonymous = True)
    rospy.spin()


