
import sys
import threading
#import rospy
#from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap, QTransform, QPainter, QBrush
from multiprocessing import Process

battery = 82
lat = 40
lng = -110
speed = 5.7
direction = 0

temp = 100.65
pitch = 50
roll = 104
radio = 15
error = "None"

spacing = 10

size = "20pt"

#Set color
rollColor = "green";
pitchColor = "green";
tempColor = "green";
radioColor = "green";
piErrColor = "red";

#Box Size
width = 250
height = 100



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


class RollBox(QVBoxLayout):

    def __init__(self):
        super(RollBox, self).__init__()
        layout = QVBoxLayout()
       
        tempLabel = QLabel("Roll:\n%.2f" % roll)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + rollColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
              
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)

      

class PitchBox(QVBoxLayout):

    def __init__(self):
        super(PitchBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Pitch:\n%.2f" % pitch)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + pitchColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)


class TempBox(QVBoxLayout):

    def __init__(self):
        super(TempBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Temperature:\n%.2fF" % temp)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + tempColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)


class RadioBox(QVBoxLayout):

    def __init__(self):
        super(RadioBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Radio Strength:\n%.2fdB" % radio)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + radioColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)

class PiErrBox(QVBoxLayout):

    def __init__(self):
        super(PiErrBox, self).__init__()

        layout = QVBoxLayout()
    
        tempLabel = QLabel("Pi Error:\n" + error)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: " + piErrColor + "; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
        
        tempLabel.setFixedSize(width, height)

        layout.addSpacing(spacing)
        #layout.setSpacing(0)
        self.addLayout(layout)
        

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: black; color: white; font-size: 24pt; font-family: Segoe UI; font-weight: 600;")
        self.setWindowTitle("Status Box")
        self.setGeometry(0, 0, 1400, 1400)
        layout = gui_rover_status()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class gui_rover_status(QVBoxLayout):
    def __init__(self):
        super(gui_rover_status, self).__init__()
        self.addLayout(RollBox())
        self.addLayout(PitchBox())
        self.addLayout(TempBox())
        self.addLayout(RadioBox())
        self.addLayout(PiErrBox())

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