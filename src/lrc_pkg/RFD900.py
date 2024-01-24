import time
import serial
import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image

class RFD900:

    def __init__(self,serialPort, baudRate=57600, netID=25, deploy=False):
        """
        This function is used to initialize class variables and to set up the default radio registers that are determined by the parameters passed in though this constructor.

        :param serialPort: This is the serial port that connects to the communications board
        :type serialPort: String, Required
        :param baudRate: This is the baud rate for the serial port
        :type baudRate: int, defaults to 57600
        :param netID: This is the radio network ID the base and the rover modems should be on the same network
        :type netID: int, defaults to 35
        :param deploy: This is a boolean toggle that determines if the netID is stored in EEPROM or not
        :type deploy: bool, defaults to false
        """
        # initalize out internal variables and set up the publisher node and comm port!!
        self.__baudRate__   = baudRate
        self.port           = serial.Serial(serialPort,self.__baudRate__, timeout=5)           # Open the serial com port
        self.dataOutBuffer  = ""
        self.dataInBuffer   = ""
        self.__imageStreamOK__  = False
        self.__imageResolution__ = [0,0]

        # Update operation registers and store final values
        if deploy:
            self.__ATCommand__(["ATS3="+str(netID), "AT&W"])
        else:
            self.__ATCommand__(["ATS3="+str(netID)])

        # Get the current parameters and save them to the class and create a UID
        self.__params__ = self.__ATCommand__(["ATI5"])
        self.deviceID   = str(netID) + ":" + self.__params__["S15"]

        if str(netID) not in self.__params__["S3"]:
            self.__errorHandler__(IOError("NetID Configuration FAIL"))
        
    def writeImage(self, dataIn: Image):
        """
        This function writes an image to the modem. This is done by writing out the image row by row.

        :param dataIn: This is the image to be written
        :type dataIn: std_msgs.msg.Image, Required

        :return: Returns a boolean value that indicates if the data was written or not
        :rtype: boolean
        """
        imageMat = dataIn.data
        if(self.__imageStreamOK__):
            # Write a row of image data at a time
            for i in range(self.__imageResolution__[0]):
                line = ""
                for j in range(self.__imageResolution__[1]):
                    line = line + "," + hex(imageMat[i][j])
                self.__writeOutgoingData__(line)
            return True
        else:
            self.__errorHandler__(RuntimeError("No Image Stream Initialization!! Please call RFD900.openImageStream()"))
            return False

    def readImage(self):
        """
        This function reads in an image from the modem. This is done by reading in the image row by row.

        :return: Returns the image matrix if one exists, else None
        :rtype: numpy matrix or None
        """
        if(self.__imageStreamOK__):
            # Read a row of image data at a time
            dataIn = np.zeros(self.__imageResolution__)
            for i in range(self.__imageResolution__[0]):
                line = self.__readIncomingData__()
                for j in range(self.__imageResolution__[1]):
                    pixel = line.split(",")
                    dataIn[i,j] = int(pixel[0])
                    line = pixel[1]
            return dataIn
        else:
            self.__errorHandler__(RuntimeError("No Image Stream Initialization!! Please call RFD900.openImageStream()"))
            return None

    def openImageStream(self, resolution):
        """
        This function sets the resolution of the expected image. It also sets an indicator used to verify that the resolution has been set before any read or write call.

        :param resolution: the resolution of the image
        :type resolution: [int, int], Required
        :return: Return true to indicate that it was set properly
        :rtype: Boolean 
        """
        self.__imageStreamOK__ = True
        self.__imageResolution__ = resolution
        return True

    def readString(self):
        """
        Read the input from the com port and set the data in buffer
        :return: the read message
        :rtype: string
        """

        pub = rospy.Publisher(self.__pullTopic__, String, queue_size = 10)
        # Will freeze if no data is passed

        self.dataInBuffer = self.__readIncomingData__()
        
        rospy.loginfo("Base To Rover:" + self.dataInBuffer)
        pub.publish(self.dataInBuffer)
        return self.dataInBuffer
        
    def writeString(self, dataIn: String):
        """
        Write data to the serial port
        :return: Returns a boolean value that indicates if the send was successful or not
        :rtype: Boolean
        """
        return self.__writeOutgoingData__(dataIn.data)  

    def __ATCommand__(self, commandList):
        """
        Sent an AT command to the long range comm device. This function should only be used internally for setup.

        :param commandList: This is the list of commands that will be sent to the device.
        :type commandList: a list of strings
        """
        output = {}
        try:
            for command in list(commandList):
                self.port.flushOutput()
                self.port.flushInput()
                
                time.sleep(1)
                self.__writeOutgoingData__("\r\n")
                time.sleep(0.5)
                self.__writeOutgoingData__("ATO\r\n")
                time.sleep(2)
                self.__writeOutgoingData__("+++")
                time.sleep(1)
                modeConf = self.__readIncomingData__()
                if("OK" in modeConf):
                    self.__writeOutgoingData__("%s\r\n" %command)
                    time.sleep(1)
                    echo = self.__readIncomingData__()
                    if (not(command in echo)):
                        raise IOError("Unable to get RFD900 into AT mode: Echo command does not match!")
                    self.__writeOutgoingData__("ATO\r\n") # not sure why its the terminate command but it is
                    time.sleep(1)
                    result = self.__readIncomingData__()
                    while "ATO" not in result:
                        if "ATI5" in command:
                            output[result.split(":")[0]]= result.split("=")[1].replace("\r","")
                        else:
                            output[command] = result
                        result = self.__readIncomingData__()
                        time.sleep(0.1)
                    
                else:
                    self.__writeOutgoingData__("ATZ\r\n")
                    raise ConnectionError("Unable to get RFD900 into AT mode, restarting")
            
        except Exception as e:
            output = "ERROR"
            self.__errorHandler__(e)

        return output

    def __readIncomingData__(self):
        """
        Read incoming data from the serial port
        :return: This function will return the data from the serial port or an error if it was not received properly
        :rtype: String
        """
        try:
            ser_bytes = self.port.read_until() # freezes with no data
            ser_bytes = ser_bytes[:len(ser_bytes)-1]
            return ser_bytes.decode()
        except Exception as e:
            return e
    
    def __writeOutgoingData__(self, data: String):
        """
        Write data to the serial port
        :param data: The data to send out
        :type data: String 
        """
        try:
            for i in range(len(data)):
                self.port.write(bytes(data[i], 'utf-8'))
            return True
        except Exception as e:
            self.__errorHandler__(e)
            return False

    def __errorHandler__(self,errorMessage):
        """
        Creates an error message and posts it to rospy log
        """
        rospy.loginfo("COM {} ERROR: {}".format(self.deviceID,errorMessage))
        


     


