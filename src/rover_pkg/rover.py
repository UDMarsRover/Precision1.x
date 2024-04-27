"""
Created By: Greg Molskow
Use Case:   To be used by the University of Dayton Mars Rover Team as a base class to define the sensors of the rover 
            and to interact with each of its parts. This code is approved for use only by UDMRT and its affiliates. 
"""

import rospy
import sys
import time
import os
from std_msgs.msg import String
import RPi.GPIO as gpio
from diagnositc_msgs.msg import Diagnostic_Status as diag



class Rover:
    def __init__(self, refreshRate:int=10, name:str="precision1"):
        self.wifiConnected = False
        self.rate = rospy.Rate(refreshRate)  # Hz
        self.name = name
        self.kill=False


        self.__indicatorLED__ = {"red": 22, "green": 27, "blue": 17}
        self.__shutdownPin__ = 13
        self.__relay__ = 26
        
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.__indicatorLED__["red"], gpio.OUT)
        gpio.setup(self.__indicatorLED__["green"], gpio.OUT)
        gpio.setup(self.__indicatorLED__["blue"], gpio.OUT)
        gpio.setup(self.__relay__,gpio.OUT)
        gpio.output(self.__relay__,1)
        gpio.setup(self.__shutdownPin__, gpio.IN)

        self.led_control(1,0,0)
        time.sleep(0.5)
        self.led_control(0,1,0)
        time.sleep(0.5)
        self.led_control(0,0,1)
        time.sleep(0.5)
        self.led_control(1,1,1)
        time.sleep(2)

        # Initialize the Rover ROS_MAIN node
        rospy.init_node(name, anonymous=True)
        self.rate = rospy.Rate(10)  # Hz
        

        self.led_control(1, 0, 0)
        while not self.wifiCheck():
            self.led_control(1, 0, 0)
            self.shutdownCheck()
        
        while rospy.is_shutdown():
            self.led_control(0,1,1)
        
        rospy.Subscriber("",diag, self.rollOverCheck)

    def spin(self):
        if self.kill: self.led_control(1,1,0)
        if rospy.is_shutdown(): self.kill=True
        self.shutdownCheck()
        if not self.wifiCheck(): self.led_control(1,0,0)
        self.rate.sleep()

    def shutdown(self):
        gpio.output(self.__relay__,0)

    def led_control(self, r: int, g: int, b: int):
        gpio.output(self.__indicatorLED__["red"], r)
        gpio.output(self.__indicatorLED__["green"], g)
        gpio.output(self.__indicatorLED__["blue"], b)

    def rollOverCheck(self, data:diag):
        self.kill = (data.level == 2)   

    def shutdownCheck(self, force: bool = False):
        if not force:
            if not gpio.input(self.__shutdownPin__):
                rospy.signal_shutdown("Rover Shutdown Button Pressed")
                self.kill = True
                return True
            else: return False
                
        else:
            self.led_control(1, 1, 0)
            rospy.signal_shutdown("Rover Shutdown Button Pressed")
            time.sleep(0.5)
            self.shutdown()
            return True 
    
    def wifiCheck(self, ip:str = "192.168.8.1"):
        return os.system(f"ping -c 1 "+ip) == 0


# end
