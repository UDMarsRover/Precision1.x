
import sys
import threading
#import rospy
#from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QPixmap, QTransform, QPainter, QBrush
from multiprocessing import Process

import datetime


spacing = 10

size = "20pt"



#Box Size
width = 250
height = 100

dateDisp = ""
timeDisp = ""

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


def TandD():
    while(True):
        now = datetime.datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%Y")

        ampm = now.strftime("%p")
        hour = now.strftime("%I")
        min = now.strftime("%M")
        sec = now.strftime("%S")

        dateDisp = month + "/" + day + "/" + year
        timeDisp = hour + ":" + min + ":" + sec + " " + ampm


        print("TandD")
        time.sleep(10)




class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class TimeDateBox(QVBoxLayout):

    def __init__(self):
        super(TimeDateBox, self).__init__()


        layout = QVBoxLayout()

        #time.sleep(10)
       
        tempLabel = QLabel(dateDisp + "\n" + timeDisp)
        layout.addWidget(tempLabel)
        tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        tempLabel.setStyleSheet("background-color: red; color: white; font-size: " + size + "; font-family: Segoe UI; font-weight: 600; border-radius: 7px")
              
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
        self.addLayout(TimeDateBox())
        
    def show(self):
        return self



if __name__ == "__main__":

    #time_thread = threading.Thread(target=TandD)
    #time_thread.start()
    p = Process(target=TandD)
    p.start()
    p.join()


    ros_thread = threading.Thread(target=listener)
    
    ros_thread.start()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
        
    #guiWindowProcess = Process(target=app.exec)
    #listenerProcess = Process(target=listener)
    #guiWindowProcess.start()
    #listenerProcess.start()