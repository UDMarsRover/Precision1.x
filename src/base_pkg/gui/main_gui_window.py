from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout
from lidar.lidar_widget import LidarWidget
import sys
#import rospy
import threading
#from sensor_msgs.msg import LaserScan
import gui_per_1 as per1
import gui_per_2 as per2
import date_time as dt
import rover_status as rstat


class udmrt_gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UD Mars Rover Team GUI")
        self.layout = QGridLayout(self)
        # Initialize widgets here.
        self.lidar_widget = LidarWidget(6.0) # Your widget
        self.lidar_widget_2 = LidarWidget(2.0) # Your widget
        self.layout.addWidget(self.lidar_widget, 0, 1) # Add to the layout
        self.layout.addWidget(self.lidar_widget_2, 0, 2) # Add to the layout
        #self.start_ros_thread()

        self.layout.addLayout(per1.gui_rover_status(),0,0)
        #self.layout.addLayout(per1.PitchBox(),1,0)
        #self.layout.addLayout(per1.TempBox(),2,0)
        self.layout.addLayout(per1.RadioBox(),1,0)
        self.layout.addLayout(per1.PiErrBox(),3,0)

        self.layout.addLayout(per2.gui_rover_status1(),3,1)
        self.layout.addLayout(per2.gui_rover_status2(),3,2)
        #self.layout.addLayout(per2.DriveBox(),4,2)
        
        

        self.layout.addLayout(rstat.gui_rover_status1(),1,1)
        self.layout.addLayout(rstat.gui_rover_status2(),1,2)


        #self.layout.addLayout(dt.TimeDateBox(),3,3)


    #def start_ros_thread(self):
        #rospy.init_node("udmrt_gui_node", anonymous=True)
        #self.ros_thread = threading.Thread(target=self.update_from_ros)
        #self.ros_thread.start()

    #def update_from_ros(self):
        #laser_subscriber = rospy.Subscriber("scan", LaserScan, self.lidar_widget.ros_callback)
        #rospy.spin()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = udmrt_gui()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()