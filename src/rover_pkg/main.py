#!/usr/bin/env python3
import time
import rospy
import sys
import os
from std_msgs.msg import String
#from rover import Rover as Presision1
import RPi.GPIO as gpio
import dbus
sys_bus = dbus.SystemBus()
lg = sys_bus.get_object('org.freedesktop.login1','/org/freedesktop/login1')
pwr_mgmt =  dbus.Interface(lg,'org.freedesktop.login1.Manager')
shutdown_method = pwr_mgmt.get_dbus_method("PowerOff")




# Create a rover instance
rate = 10  # Hz
#p1 = Presision1(rate)
gpio.setmode(gpio.BCM)

indicatorLED = {"red": 22, "green": 27, "blue": 17}
shutdownPin = 13

gpio.setup(indicatorLED["red"], gpio.OUT)
gpio.setup(indicatorLED["green"], gpio.OUT)
gpio.setup(indicatorLED["blue"], gpio.OUT)
gpio.setup(shutdownPin, gpio.IN)


def led_control(r: int, g: int, b: int):
    gpio.output(indicatorLED["red"], r)
    gpio.output(indicatorLED["green"], g)
    gpio.output(indicatorLED["blue"], b)


def shutdown(check: bool = True):
    if check:
        if not gpio.input(shutdownPin):
            led_control(1, 1, 0)
            #os.system("systemctl poweroff")
            shutdown_method(True)
            
    else:
        led_control(1, 1, 0)
        #os.system("systemctl poweroff")
        #stop_method()
        shutdown_method(True)
        


# The main Loop
if __name__ == "__main__":
    while os.system(f"ping -c 1 192.168.8.1") == 1:
        led_control(1, 0, 0)
        shutdown()

   

    # While roscore is running
    while not rospy.is_shutdown():
        led_control(0, 1, 0)
        shutdown()
        #if p1.hasError():
        #    print(" i seem to has an ewwow :( plz hewp me :,(...." + p1.getError())
        #else:
        #    p1.publishDataToBase()

        # Sleep for a set amount of time to keep our rate
        #p1.rate.sleep()

    shutdown(False)
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
    print("!!!!!.....ROS IS SHUTDOWN.....!!!!!")
