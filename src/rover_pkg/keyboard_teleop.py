import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Accel, Vector3

rospy.init_node('RoverKeyboard', anonymous=True)
pub = rospy.Publisher('DriveVelocity', Accel, queue_size=10)

while(True):
    v = float(input("Input Linear Vel(m/s):"))
    w = float(input("Input Angular Vel(deg/s):"))
    lv = Vector3()
    lv.x = v

    wv = Vector3()
    wv.x = w

    pub.publish(lv,wv)
    print([v,w])
