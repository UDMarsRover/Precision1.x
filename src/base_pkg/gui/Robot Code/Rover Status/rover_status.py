
import sys
import threading
import rospy
from sensor_msgs.msg import NavSatFix, BatteryState
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap, QTransform
from multiprocessing import Process

battery = 82
lat = 40
lng = -110
speed = 5.7
direction = 0



def callbackGPS(NavSatFix):
    global lat, lng
    lat = NavSatFix.latitude
    lng = NavSatFix.longitude

def callbackBAT(BatteryStatus):
    global battery
    battery = int(BatteryStatus.percentage * 100)

rospy.init_node('listener', anonymous=True)

def listener():
    #rospy.Subscriber("DriveCommand", Accel, callback)
    #rospy.Subscriber("gps", NavSatFix, callback)
    rospy.Subscriber("GPS", NavSatFix, callbackGPS)
    rospy.Subscriber("BatteryStatus", BatteryState, callbackBAT)
    rospy.spin()
    print("listener")




class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class BatteryBox(QVBoxLayout):

    def __init__(self):
        super(BatteryBox, self).__init__()

        batteryImage = QLabel()
        pixmap = QPixmap('batteryicon.png')
        batteryImage.setPixmap(pixmap)
        self.addWidget(batteryImage)
        batteryImage.setAlignment(QtCore.Qt.AlignCenter)

        batteryLabel = QLabel("%d%%" % battery)
        batteryLabel.setStyleSheet("background: none; font-size: 40pt; font-weight: 600;")

        subLayout = QHBoxLayout()
        subLayout.addWidget(batteryLabel)
        batteryLabel.setAlignment(QtCore.Qt.AlignCenter)
        batteryImage.setLayout(subLayout)

        batteryImage.stackUnder(batteryLabel)

class CoordsBox(QHBoxLayout):

    def __init__(self):
        super(CoordsBox, self).__init__()

        layout = QVBoxLayout()

        latLabel = QLabel("%.6f " % abs(lat))
        if lat >= 0:
            latLabel.setText(latLabel.text() + "N")
        else:
            latLabel.setText(latLabel.text() + "S")
        layout.addWidget(latLabel)
        latLabel.setAlignment(QtCore.Qt.AlignCenter)

        lngLabel = QLabel("%.6f " % abs(lng))
        if lng <= 0:
            lngLabel.setText(lngLabel.text() + "W")
        else:
            lngLabel.setText(lngLabel.text() + "E")
        layout.addWidget(lngLabel)
        lngLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.addLayout(layout)

class SpeedBox(QHBoxLayout):

    def __init__(self):
        super(SpeedBox, self).__init__()

        layout = QVBoxLayout()

        speedLabel = QLabel("%.2f" % speed)
        layout.addWidget(speedLabel)
        speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        speedLabel.setStyleSheet("font-size: 40pt; font-weight: 600;")

        mphLabel = QLabel("MPH")
        layout.addWidget(mphLabel)
        mphLabel.setAlignment(QtCore.Qt.AlignCenter)
        mphLabel.setStyleSheet("font-size: 16pt;")

        layout.setSpacing(0)
        self.addLayout(layout)

class DirectionBox(QHBoxLayout):

    def __init__(self):
        super(DirectionBox, self).__init__()

        layout = QHBoxLayout()

        directionLabel = QLabel("%d°" % direction)
        directionLabel.setStyleSheet("font-size: 40pt; font-weight: 600;")
        layout.addWidget(directionLabel)
        directionLabel.setAlignment(QtCore.Qt.AlignCenter)

        compassLabel = QLabel()
        pixmap = QPixmap('compassrose.png')
        transform = QTransform().rotate(-direction)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        compassLabel.setPixmap(pixmap)


        layout.addWidget(compassLabel)

        self.addLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: black; color: white; font-size: 24pt; font-family: Segoe UI; font-weight: 600;")
        self.setWindowTitle("Status Box")
        self.setGeometry(0, 0, 1200, 150)
        layout = gui_rover_status()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class gui_rover_status(QHBoxLayout):
    def __init__(self):
        super(gui_rover_status, self).__init__()
        self.addLayout(BatteryBox())
        self.addLayout(CoordsBox())
        self.addLayout(SpeedBox())
        self.addLayout(DirectionBox())

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
