import rospy
from sensor_msgs.msg import LaserScan
from ouster_sdk.examples.python.lidarscan import LidarScan

class LidarProcessor(object):
    def __init__(self):
        # create a subscriber to the /scan topic
        self.scan_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback)
        # create a publisher to another topic
        self.object_pub = rospy.Publisher("/objects", ObjectArray, queue_size=10)
        # create a lidarscan object
        self.lidar = LidarScan()

    def scan_callback(self, msg):
        # convert the laserscan message to a lidarscan object
        self.lidar.from_msg(msg)
        # apply some noise filters to the lidarscan data
        self.lidar.apply_noise_filter()
        # get the angle, distance and width of the 5 closest objects
        objects = self.lidar.get_closest_objects(5)
        # publish the objects to another topic
        self.object_pub.publish(objects)

    def run(self):
        # initialize a node
        rospy.init_node("lidar_processor")
        # spin until interrupted
        rospy.spin()