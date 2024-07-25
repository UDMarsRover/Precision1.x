
import sys
import threading
#import rospy
#from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap, QTransform, QPainter, QBrush
from multiprocessing import Process

battery = 82
lat = 40
lng = -110
speed = 5.7
direction = 0

emoErr = "None"
driveErr = "None"
armErr = "None"
cameraErr = "None"

spacing = 5

size = "20pt"

#Set Color
emoColor = "green";
driveColor = "green";
armColor = "green";
cameraColor = "green";

#Box Size
width = 240
height = 90


def callbackGPS(NavSatFix):
    global lat, lng
    lat = NavSatFix.latitude
    lng = NavSatFix.longitude

def callbackBAT(BatteryStatus):
    global battery
    battery = int(BatteryStatus.percentage * 100)

#rospy.init_node('listener', anonymous=True)

def listener():
    #rospy.Subscriber("DriveCommand", Accel, callback)
    #rospy.Subscriber("gps", NavSatFix, callback)
    #rospy.Subscriber("GPS", NavSatFix, callbackGPS)
    #rospy.Subscriber("BatteryStatus", BatteryState, callbackBAT)
    #rospy.spin()
    print("listener")




class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class EmoBox(QVBoxLayout):

    def __init__(self):
        super(EmoBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Emo Error:\n" + emoErr)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + emoColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        #layout.setSpacing(100)
        layout.addSpacing(spacing)
        self.addLayout(layout)


class DriveBox(QVBoxLayout):

    def __init__(self):
        super(DriveBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Drive Error:\n" + driveErr)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + driveColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)


class ArmBox(QVBoxLayout):

    def __init__(self):
        super(ArmBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Arm Error:\n" + armErr)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + armColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)


class CameraBox(QVBoxLayout):

    def __init__(self):
        super(CameraBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Camera Error:\n" + cameraErr)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + cameraColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px;")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)
        

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: black; color: white; font-size: 24pt; font-family: Segoe UI; font-weight: 600;")
        self.setWindowTitle("Status Box")
        self.setGeometry(0, 0, 1000, 400)
        layout = gui_rover_status()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class gui_rover_status1(QHBoxLayout):
    def __init__(self):
        super(gui_rover_status1, self).__init__()
        self.addLayout(EmoBox())
        self.addLayout(DriveBox())

class gui_rover_status2(QHBoxLayout):
    def __init__(self):
        super(gui_rover_status2, self).__init__()
        self.addLayout(ArmBox())
        self.addLayout(CameraBox())

    def show(self):
        return self



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    ros_thread = threading.Thread(target=listener)
    ros_thread.start()

    app.exec()
        
    #guiWindowProcess = Process(target=app.exec)
    #listenerProcess = Process(target=listener)
    #guiWindowProcess.start()
    #listenerProcess.start()