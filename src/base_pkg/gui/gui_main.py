<<<<<<< HEAD
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QStackedLayout
 )

from PyQt5.QtGui import QPalette, QColor

class P(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(600, 200))

        layout = QHBoxLayout()

        emoLabel = QLabel("Emo Error")
        emoLabel.setStyleSheet("background-color: red; color: white;")
        emoLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(emoLabel)

        driveLabel = QLabel("Drive Error")
        driveLabel.setStyleSheet("background-color: red; color: white;")
        driveLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(driveLabel)

        armLabel = QLabel("Arm Error")
        armLabel.setStyleSheet("background-color: red; color: white")
        armLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(armLabel)

        camLabel = QLabel("Camera Error")
        camLabel.setStyleSheet("background-color: red; color: white")
        camLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(camLabel)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
=======
import gui_per_1 as per1
import gui_per_2 as per2

import sys
import threading
#import rospy
#from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
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
        self.setGeometry(0, 0, 1400, 1400)
        layout1 = gui_pers()
       # layout2 = gui_per_2()

        widget1 = QWidget()
        #widget2 = QWidget()
        widget1.setLayout(layout1)
        #widget2.setLayout(layout2)
        self.setCentralWidget(widget1)
       # self.setCentralWidget(widget2)


class gui_rover_status(QVBoxLayout):
    def __init__(self):
        super(gui_rover_status, self).__init__()
        self.addLayout(per1.RollBox())
        self.addLayout(per1.PitchBox())
        self.addLayout(per1.TempBox())
        self.addLayout(per1.RadioBox())
        self.addLayout(per1.PiErrBox())
        
class gui_per_2(QHBoxLayout):
    def __init__(self):
        super(gui_per_2, self).__init__()
        self.addLayout(per2.EmoBox())
        self.addLayout(per2.DriveBox())
        self.addLayout(per2.ArmBox())
        self.addLayout(per2.CameraBox())

class gui_pers(QVBoxLayout):
    def __init__(self):
        super(gui_pers, self).__init__()
        self.addLayout(gui_rover_status())
        self.addLayout(gui_per_2())
        

def show(self):
    return self


>>>>>>> cd9b0e05b26f0b2f0eb55c811c6ab04a0d93c313

if __name__ == "__main__":

    app = QApplication(sys.argv)
<<<<<<< HEAD
    window = P()
    window.show()

    app.exec()
=======

    window = MainWindow()
    window.show()

    ros_thread = threading.Thread(target=listener)
    ros_thread.start()

    app.exec()

>>>>>>> cd9b0e05b26f0b2f0eb55c811c6ab04a0d93c313
