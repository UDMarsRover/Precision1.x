#Composes and decomposes the messageOuts sent between rover and base

class UDMRTDataBuffer:

    def __init__(self):
        
        #Variables
        self.__errorMessageData__ = ""
        self.__driveMotor1Data__ = ""
        self.__driveMotor2Data__ = ""
        self.__driveMotor3Data__ = ""
        self.__driveMotor4Data__ = ""
        self.__armMotor1Data__ = ""
        self.__armMotor2Data__ = ""
        self.__armMotor3Data__ = ""
        self.__armMotor4Data__ = ""
        self.__armMotor5Data__ = ""
        self.__armMotor6Data__ = ""
        self.__gyroscopeData__ = ""
        self.__boxTempData__ = ""
        self.__busMonitorData__ = ""
        self.__batteryTempData__ = ""
        self.__voltageConverterTempData__ = ""
        self.__currentConversionData__ = ""
        self.__ultrasonicSensor1Data__ = ""
        self.__ultrasonicSensor2Data__ = ""
        self.__ultrasonicSensor3Data__ = ""
        self.__ultrasonicSensor4Data__ = ""
        
        self.__driveMotorErrorData__ = ""
        self.__armMotorErrorData__ = ""
        self.__emoErrorData__ = ""
        self.__cameraData__ = ""

        self.__messageOut__ = ""
        
    #Getter and setter methods... lots of them...
    
    def setErrorMessageData(self):
        # Do some logic for determining error code 
        emo     = self.__emoErrorData__
        drive   = self.__driveMotorErrorData__
        arm     = self.__armMotorErrorData__

        if (emo != "FF"):
            self.__errorMessageData__ = emo
        elif (drive != "FF"):
            self.__errorMessageData__ = drive
        elif (arm != "FF"):
            self.__errorMessageData__ = arm
        else:
            self.__errorMessageData__ = "FF"
        
    
    def getErrorMessageData(self):
        return self.__errorMessageData__
    
    def getDriveMotorData(self):
        strOut = self.__driveMotor1Data__
        strOut += self.__driveMotor2Data__
        strOut += self.__driveMotor3Data__
        strOut += self.__driveMotor4Data__
        return strOut

    def getDriveMotor1Data(self):
        return self.__driveMotor1__
    
    def getDriveMotor2Data(self):
        return self.__driveMotor2__
    
    def getDriveMotor3Data(self):
        return self.__driveMotor3__
    
    def getDriveMotor4Data(self):
        return self.__driveMotor4__

    def getArmMotorData(self):
        strOut = self.__armMotor1Data__
        strOut += self.__armMotor2Data__
        strOut += self.__armMotor3Data__
        strOut += self.__armMotor4Data__
        strOut += self.__armMotor5Data__
        strOut += self.__armMotor6Data__


    def getArmMotor1Data(self):
        return self.__armMotor1__
    
    def getArmMotor2Data(self):
        return self.__armMotor2__
    
    def getArmMotor3Data(self):
        return self.__armMotor3__
    
    def getArmMotor4Data(self):
        return self.__armMotor4__
    
    def getArmMotor5Data(self):
        return self.__armMotor5__
    
    def getArmMotor6Data(self):
        return self.__armMotor6__
    
    def getGyroscopeData(self):
        return self.__gyroscopeData__
    
    def getBoxTempData(self):
        return self.__boxTempData__
    
    def getBusMonitorData(self):
        return self.__busMonitorData__
    
    def getBatteryTempData(self):
        return self.__batteryTempData__
    
    def getVoltageConverterTempData(self):
        return self.__voltageConverterTempData__
    
    def getCurrentConversionData(self):
        return self.__currentConversionData__
    
    def getUltrasonicSensor1Data(self):
        return self.__ultrasonicSensor1Data__
    
    def getUltrasonicSensor2Data(self):
        return self.__ultrasonicSensor2Data__
    
    def getUltrasonicSensor3Data(self):
        return self.__ultrasonicSensor3Data__
    
    def getUltrasonicSensor4Data(self):
        return self.__ultrasonicSensor4Data__

    def getEmoData(self):
        strOut = self.getGyroscopeData()
        strOut += self.getBoxTempData()
        strOut += self.getBusMonitorData()
        strOut += self.getBatteryTempData()
        strOut += self.getVoltageConverterTempData()
        strOut += self.getCurrentConversionData()
        strOut += self.getUltrasonicSensor1Data()
        strOut += self.getUltrasonicSensor2Data()
        strOut += self.getUltrasonicSensor3Data()
        strOut += self.getUltrasonicSensor4Data()
    
    def setDriveMotorData(self, dataIn):
        str = dataIn.data
        str = str.upper()
        self.__driveMotorErrorData__ = str[0:2]
        self.__driveMotor1Data__ = str[2:5]
        self.__driveMotor2Data__ = str[5:8]
        self.__driveMotor3Data__ = str[8:11]
        self.__driveMotor4Data__ = str[11:14]
        
    def setArmMotorData(self, dataIn):
        str = dataIn.data
        str = str.upper()
        self.__armMotorErrorData__ = str[0:2]
        self.__armMotor1Data__ = str[2:7]
        self.__armMotor2Data__ = str[7:12]
        self.__armMotor3Data__ = str[12:17]
        self.__armMotor4Data__ = str[17:22]
        self.__armMotor5Data__ = str[22:27]
        self.__armMotor6Data__ = str[27:32]
        
    def setEmoData(self, dataIn):
        str = dataIn.data
        str = str.upper()
        self.__emoErrorData__ = str[0:2]
        self.__gyroscopeData__ = str[2:5]
        self.__boxTempData__ = str[5:8]
        self.__busMonitorData__ = str[8:12]
        self.__batteryTempData__ = str[12:15]
        self.__voltageConverterTempData__ = str[15:18]
        self.__currentConversionData__ = str[18:22]
        self.__ultrasonicSensor1Data__ = str[22:26]
        self.__ultrasonicSensor2Data__ = str[26:30]
        self.__ultrasonicSensor3Data__ = str[30:34]
        self.__ultrasonicSensor4Data__ = str[34:38]
        
    #def setCameraData(self, dataIn):
    #    self.__cameraData__ = dataIn.data
    
    def composeMessageOut(self):
        
        #Concatenate all of the variables together into one __messageOut__
        self.__messageOut__ += self.getErrorMessageData()
        self.__messageOut__ += self.getDriveMotor1Data()
        self.__messageOut__ += self.getDriveMotor2Data()
        self.__messageOut__ += self.getDriveMotor3Data()
        self.__messageOut__ += self.getDriveMotor4Data()
        self.__messageOut__ += self.getArmMotor1Data()
        self.__messageOut__ += self.getArmMotor2Data()
        self.__messageOut__ += self.getArmMotor3Data()
        self.__messageOut__ += self.getArmMotor4Data()
        self.__messageOut__ += self.getArmMotor5Data()
        self.__messageOut__ += self.getArmMotor6Data()
        self.__messageOut__ += self.getGyroscopeData()
        self.__messageOut__ += self.getBoxTempData()
        self.__messageOut__ += self.getBusMonitorData()
        self.__messageOut__ += self.getBatteryTempData()
        self.__messageOut__ += self.getVoltageConverterTempData()
        self.__messageOut__ += self.getCurrentConversionData()
        self.__messageOut__ += self.getUltrasonicSensor1Data()
        self.__messageOut__ += self.getUltrasonicSensor2Data()
        self.__messageOut__ += self.getUltrasonicSensor3Data()
        self.__messageOut__ += self.getUltrasonicSensor4Data()
        
        return self.__messageOut__
    
    #Checking for any errors
    def checkForError(self):
        #If true, no error. If false, there is an error.
        return self.__errorMessageData__ == "FF"
