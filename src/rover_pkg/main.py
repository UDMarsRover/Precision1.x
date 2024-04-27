#!/usr/bin/env python3
import time
import rospy
import rostopic
import sys
import os
from std_msgs.msg import String
#from rover import Rover as Presision1
import RPi.GPIO as gpio
from pydbus import SystemBus
bus = SystemBus()

proxy = bus.get('org.freedesktop.login1', '/org/freedesktop/login1')





# Create a rover instance

#p1 = Presision1(rate)
gpio.setmode(gpio.BCM)

indicatorLED = {"red": 22, "green": 27, "blue": 17}
shutdownPin = 13
relay = 26
wifiConnected = False

gpio.setwarnings(False)
gpio.setup(indicatorLED["red"], gpio.OUT)
gpio.setup(indicatorLED["green"], gpio.OUT)
gpio.setup(indicatorLED["blue"], gpio.OUT)
gpio.setup(relay,gpio.OUT)
gpio.output(relay,1)
gpio.setup(shutdownPin, gpio.IN)


def led_control(r: int, g: int, b: int):
    gpio.output(indicatorLED["red"], r)
    gpio.output(indicatorLED["green"], g)
    gpio.output(indicatorLED["blue"], b)


def shutdown(check: bool = True):
    if check:
        if not gpio.input(shutdownPin):
            led_control(1, 1, 0)
            rospy.signal_shutdown("Rover Shutdown Button Pressed")
            while not gpio.input(shutdownPin): None
            gpio.output(relay,0)
            return True
        else: return False
            
    else:
        led_control(1, 1, 0)
        rospy.signal_shutdown("Rover Shutdown Button Pressed")
        time.sleep(0.5)
        gpio.output(relay,0)
        return True
        
def wifiCheck(ip:str = "192.168.8.1"):
    return os.system(f"ping -c 1 "+ip) == 0


# The main Loop
if __name__ == "__main__":
    led_control(1,0,0)
    time.sleep(0.5)
    led_control(0,1,0)
    time.sleep(0.5)
    led_control(0,0,1)
    time.sleep(0.5)
    led_control(1,1,1)
    time.sleep(2)

    rospy.init_node("precision1")
    rate = rospy.Rate(10)  # Hz

    led_control(1, 0, 0)
    while not wifiCheck():
        led_control(1, 0, 0)
        shutdown()


    # While roscore is running
    while not shutdown():
        while not rospy.is_shutdown():
            if wifiCheck(): led_control(0, 1, 0)
            else: led_control(1,0,0)
            shutdown()
            rate.sleep

        led_control(0,1,1)

    
    print("DEAD")
