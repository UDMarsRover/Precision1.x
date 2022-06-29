import time
import serial
import rospy
from std_msgs.msg import String as rosstring

class Communications:

    def __init__(self,name,serialPort, baudRate=57600):
        # initalize out internal variables and set up the publisher node and comm port!!
        self.__subscriberName = name
        self.__baudRate     = baudRate
        self.port           = serial.Serial(serialPort,self.__baudRate)           # Open the serial com port
        self.error          = None
        self.DataOutBuffer  = ""
        self.DataInBuffer   = ""
    # Getter function for getting baud rate
    def getBaud(self):
        return self.__baudRate
    
    # Send data out
    def writeData(self):
        try:
            for i in range(0,len(self.DataOutBuffer)):
                self.port.write(bytes(self.DataOutBuffer[i],'utf-8'))         # Write the data to the comms device
            
            self.port.write(bytes('\n','utf-8'))            # Write our termination value to indicate the message is over
        except Exception as e:
            self.error = e
        

    # Check to see if there is data that was sent to the reciver
    def readData(self):
        
        # Will freeze if no data is passed

        try:
            ser_bytes = self.port.read_until()
            ser_bytes = ser_bytes[:len(ser_bytes)-1]
            self.DataInBuffer = ser_bytes.decode()
        
        except Exception as e:
            self.error = e
            

        return self.DataInBuffer
     


