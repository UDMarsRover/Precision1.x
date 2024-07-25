import gui_per_1 as per1
import gui_per_2 as per2
#import main_gui_window as lidar
import lidar.lidar_widget as lidar

import sys
import threading
#import rospy
#from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap, QTransform, QPainter, QBrush
from multiprocessing import Process

def listener():
    #rospy.Subscriber("DriveCommand", Accel, callback)
    #rospy.Subscriber("gps", NavSatFix, callback)
    #rospy.Subscriber("GPS", NavSatFix, callbackGPS)
    #rospy.Subscriber("BatteryStatus", BatteryState, callbackBAT)
    #rospy.spin()
    print("listener")

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: black; color: white; font-size: 24pt; font-family: Segoe UI; font-weight: 600;")
        self.setWindowTitle("Status Box")
        self.setGeometry(0, 0, 1000, 400)
        #layout = pers()
        layout = QGridLayout()
        layout.addLayout(per1.RollBox(),0,0)
        layout.addLayout(per1.PitchBox(),1,0)
        layout.addLayout(per1.TempBox(),2,0)
        layout.addLayout(per1.RadioBox(),3,0)
        layout.addLayout(per1.PiErrBox(),4,0)

        layout.addLayout(per2.EmoBox(),4,1)
        layout.addLayout(per2.DriveBox(),4,2)
        layout.addLayout(per2.ArmBox(),4,3)
        layout.addLayout(per2.CameraBox(),4,4)

        layout.addLayout(lidar.LidarWidget(6.0),1,2)
        

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

class pers(QVBoxLayout):

    def __init__(self):
        super(pers, self).__init__()
        self.addLayout(per1.gui_rover_status())
        self.addLayout(per2.CameraBox())






def show(self):
    return self

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    ros_thread = threading.Thread(target=listener)
    ros_thread.start()

    app.exec()

