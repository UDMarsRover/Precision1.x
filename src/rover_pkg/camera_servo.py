import rospy
from std_msgs.msg import Int8
import time

class CameraServoNode:
    def __init__(self):
        self.servo_pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.p = GPIO.PWM(self.servo_pin, 50)
        self.p.start(2.5) # duty cycle 2.5%
        rospy.init_node("camera_servo_node", anonymous=True)
        self.sub = rospy.Subscriber("/base/gui/out/camera_servo", Int8, self.callback)

    def callback(self, msg):
        self.p.ChangeDutyCycle(msg.data)

    def stop(self):
        self.p.stop()
        GPIO.cleanup()
        

def main(args=None):
    csn = CameraServoNode()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        csn.stop()
if __name__ == "__main__":
    main()