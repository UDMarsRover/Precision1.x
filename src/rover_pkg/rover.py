"""
Created By: Greg Molskow
Use Case:   To be used by the University of Dayton Mars Rover Team as a base class to define the sensors of the rover
            and to interact with each of its parts. This code is approved for use only by UDMRT and its affiliates.
"""

import rospy
from std_msgs.msg import String
import RPi.GPIO as gpio
from diagnostic_msgs.msg import DiagnosticStatus as diag
import time
import os
import threading

class Rover:
    def __init__(self, refreshRate: int = 10, name: str = "precision1"):
        self.wifiConnected = False
        self.name = name
        self.kill = False

        self.__indicatorLED__ = {"red": 22, "green": 27, "blue": 17}
        self.__shutdownPin__ = 13
        self.__relay__ = 26
        self.__button_timer__ = 0
        self.__kill_count__ = 0

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.__indicatorLED__["red"], gpio.OUT)
        gpio.setup(self.__indicatorLED__["green"], gpio.OUT)
        gpio.setup(self.__indicatorLED__["blue"], gpio.OUT)
        gpio.setup(self.__relay__, gpio.OUT)
        gpio.output(self.__relay__, 1)
        gpio.setup(self.__shutdownPin__, gpio.IN)

        self.led_control(1, 0, 0)
        time.sleep(0.5)
        self.led_control(0, 1, 0)
        time.sleep(0.5)
        self.led_control(0, 0, 1)
        time.sleep(0.5)
        self.led_control(1, 1, 1)
        time.sleep(2)

        # Initialize the Rover ROS_MAIN node
        rospy.init_node(name, anonymous=True)
        self.rate = rospy.Rate(refreshRate)  # Hz

        self.shutdownThread = threading.Thread(target=self.shutdownThread)
        self.wifiThread = threading.Thread(target=self.wifiCheckThread)

        self.shutdownThread.start()
        self.wifiThread.start()

        self.led_control(1, 0, 0)
        while not self.wifiCheck():
            self.led_control(1, 0, 0)
            self.log("Connecting to WiFi")

        self.log("WiFi Connected")

        while rospy.is_shutdown():
            self.led_control(0, 1, 1)
            self.log("Connecting to ROS")

        self.log("Connected to ROS")

        rospy.Subscriber("/emo/status/imu", diag, self.rollOverCheck)

        self.log("Rover Started!")

    def spin(self):
        if rospy.is_shutdown():
            self.kill = True
        print(self.wifiConnected)
        if self.__kill_count__ > 0:
            self.led_control(1, 1, 0)
        elif not self.wifiConnected:
            self.led_control(1, 0, 0)
            self.log("Wifi Disconnected!")
        else:
            self.led_control(0, 1, 0)
        self.rate.sleep()

    def shutdown(self):
        gpio.output(self.__relay__, 0)

    def log(self, msg: str):
        rospy.loginfo(msg)

    def led_control(self, r: int, g: int, b: int):
        gpio.output(self.__indicatorLED__["red"], r)
        gpio.output(self.__indicatorLED__["green"], g)
        gpio.output(self.__indicatorLED__["blue"], b)

    def rollOverCheck(self, data: diag):
        self.log("Rollover Detected - Kill Requested")
        self.kill = data.level == 2

    def shutdownThread(self):
        while not rospy.is_shutdown():
            print("checking shutdown")
            self.shutdownCheck(False)
            time.sleep(0.5 )
        
    

    def shutdownCheck(self, force: bool = False):
        if not force:
            if not gpio.input(self.__shutdownPin__):
                self.led_control(1, 1, 0)
                currTime = time.time()
                if (currTime - self.__button_timer__) > 1:
                    self.__kill_count__ += 1
                    self.__button_timer__ = currTime
                if self.__kill_count__ > 5:
                    self.log("Kill Requested via Button")
                    rospy.signal_shutdown("Rover Shutdown Button Pressed")
                    self.kill = True
                return True
            else:
                self.kill = False
                self.__kill_count__ = 0
                return False

        else:
            self.led_control(1, 1, 0)
            self.log("Kill Forced")
            rospy.signal_shutdown("Rover Shutdown Button Pressed")
            time.sleep(0.5)
            self.shutdown()
            return True

    def wifiCheckThread(self):
        while not rospy.is_shutdown():
            print("checking shutdown")
            self.wifiCheck()
            time.sleep(0.5)

    def wifiCheck(self, ip: str = "192.168.8.1"):
        self.wifiConnected = os.system(f"ping -c 1 -W 100 " + ip) == 0
        return self.wifiConnected


# end
