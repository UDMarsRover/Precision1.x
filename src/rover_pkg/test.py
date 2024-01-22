import serial
import time
import rospy
from geometry_msgs.msg import Twist, Vector3

class ArduinoPort:

    def __init__(self, serialPort:str,timeoutCount:int=100,baudRate:int=9600):
        self.__serial__ = serial.Serial(serialPort,baudRate,timeout=0)

        self.__output__ = ""
        self.__timeout__ = timeoutCount
        self.__inBuff__ = ""

        self.__connectToDevice__()
    
    def getData(self):
        count = 0
        while (not self.__readPort__() and self.__timeout__ >= count): 
            count += 1
            time.sleep(0.001)
        temp = self.__output__
        self.__output__ = ""
        return temp
    
    def sendData(self, data:str):
        self.__serial__.write(bytes(data, 'utf-8')+b'4')
        temp = self.getData()
        return  temp == data

    def close(self): self.__serial__.close()
    
    def __readPort__(self):
        received = False
        while (self.__serial__.in_waiting > 0 and not received):
            data = self.__serial__.read()
            if data == b'4':
                received = True 
                self.__output__ = self.__inBuff__
                self.__inBuff__ = ""
            elif data != b'' : 
                self.__inBuff__ += data.decode() 

        return received
    

    def __reOpen__(self):
        self.__serial__.close()
        time.sleep(0.1)
        self.__serial__.open()
        time.sleep(0.5)


    def __connectToDevice__(self):
        connected = False
        while self.__serial__.in_waiting == 0:
            time.sleep(0.001)
        
        reBoots = 0
        while (not connected) and (3 >= reBoots): 
            setupCount = 0
            while (not connected) and (self.__timeout__ >= setupCount): 
                setupCount += 1
                temp = self.getData()
                connected = temp == "@S"
            if not connected: 
                self.__reOpen__()
                reBoots += 1

        if not connected: raise IOError(f'Unable to start connection with Arduino ... Make sure you have called the correct port!')

if __name__ == "__main__":
    port = ArduinoPort("/dev/ttyACM0")
    def callback(dataIn):
        vL = dataIn.linear.x
        vA = dataIn.angular.x
        output = f"{vL},{vA}"
        print(port.sendData(output))

    
    rospy.init_node('DriveArduino')
    rospy.Subscriber('DriveVelocity', Twist, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()

