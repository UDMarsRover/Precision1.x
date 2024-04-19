from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout
from lidar.lidar_widget import LidarWidget
import sys
import rospy
import threading
from sensor_msgs.msg import LaserScan


class udmrt_gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout(self)
        # Initialize widgets here.
        self.lidar_widget = LidarWidget(3.0) # Your widget
        self.lidar_widget_2 = LidarWidget(2.0) # Your widget
        self.layout.addWidget(self.lidar_widget, 0, 0) # Add to the layout
        self.layout.addWidget(self.lidar_widget_2, 0, 1) # Add to the layout
        self.start_ros_thread()

    def start_ros_thread(self):
        rospy.init_node("udmrt_gui_node", anonymous=True)
        self.ros_thread = threading.Thread(target=self.update_from_ros)
        self.ros_thread.start()

    def update_from_ros(self):
        laser_subscriber = rospy.Subscriber("scan", LaserScan, self.lidar_widget.ros_callback)
        rospy.spin()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = udmrt_gui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()