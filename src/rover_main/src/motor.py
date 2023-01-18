# This class will create a motor instace for the UDMRT Rover
# By: Greg Molskow

import rospy

# Used for serial Communications
import serial
import time

from std_msgs.msg import String


class Motors:

    class NoComPortConnection(Exception):
        pass

    
    def dataOut(self,dataIn):

        switcher={
            'w': 1,
            'a': 2,
            's': -1,
            'd': -2
        }
        
        self.arduino.write(bytes(switcher.get(dataIn.data,0),'String'))
    

    def __init__(self,comm = 'null', baud = 9600, timeout = 0.1):
        if comm != 'null':
            self.arduino = serial.Serial(port=comm, baudrate=baud, timeout=timeout)
        
        else:
            raise NoComPortConnection("Please list a com port when initializing the Motors class")

       

    