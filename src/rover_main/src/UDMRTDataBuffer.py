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
        
        self.messageOut = ""
        
    #Getter and setter methods... lots of them
    
    def setErrorMessageData(self, str):
        self.__errorMessageData__ = str
    
    def getErrorMessageData(self):
        return self.__errorMessageData__
    
    def setDriveMotor1Data(self, str):
        self.__driveMotor1__ = str
    
    def getDriveMotor1Data(self):
        return self.__driveMotor1__
    
    def setDriveMotor2Data(self, str):
        self.__driveMotor2__ = str
    
    def getDriveMotor2Data(self):
        return self.__driveMotor2__
    
    def setDriveMotor3Dat(self, str):
        self.__driveMotor3__ = str
    
    def getDriveMotor3Data(self):
        return self.__driveMotor3__
    
    def setDriveMotor4Data(self, str):
        self.__driveMotor4__ = str
    
    def getDriveMotor4Data(self):
        return self.__driveMotor4__
    
    def setArmMotor1Data(self, str):
        self.__armMotor1__ = str
    
    def getArmMotor1Data(self):
        return self.__armMotor1__
    
    def setArmMotor2Data(self, str):
        self.__armMotor2__ = str
    
    def getArmMotor2Data(self):
        return self.__armMotor2__
    
    def setArmMotor3Data(self, str):
        self.__armMotor3__ = str
    
    def getArmMotor3Data(self):
        return self.__armMotor3__
    
    def getArmMotor4Data(self, str):
        self.__armMotor4__ = str
    
    def getArmMotor4Data(self):
        return self.__armMotor4__
    
    def setArmMotor5Data(self, str):
        self.__armMotor5__ = str
    
    def getArmMotor5Data(self):
        return self.__armMotor5__
    
    def setArmMotor6Data(self, str):
        self.__armMotor6__ = str
    
    def getArmMotor6Data(self):
        return self.__armMotor6__
    
    def setGyroscopeMotorData(self, str):
        self.__gyroscopeData__ = str
    
    def getGyroscopeMotorData(self):
        return self.__gyroscopeData__
    
    def setBoxTempData(self, str):
        self.__boxTempData__ = str
    
    def getBoxTempData(self):
        return self.__boxTempData__
    
    def setBusMonitorData(self, str):
        self.__busMonitorData__ = str
    
    def getBusMonitorData(self):
        return self.__busMonitorData__
    
    def setBatteryTempData(self, str):
        self.__batteryTempData__ = str
    
    def getBatteryTempData(self):
        return self.__batteryTempData__
    
    def setVoltageConverterTempData(self, str):
        self.__voltageConverterTempData__ = str
    
    def getVoltageConverterTempData(self):
        return self.__voltageConverterTempData__
    
    def setCurrentConversionData(self, str):
        self.__currentConversionData__ = str
    
    def getCurrentConversionData(self):
        return self.__currentConversionData__
    
    def composemessageOut(self):
        
        
        #Concatenate all of the variables together into one messageOut
        self.messageOut += self.getErrorMessageData
        self.messageOut += self.getDriveMotor1Data
        self.messageOut += self.getDriveMotor2Data
        self.messageOut += self.getDriveMotor3Data
        self.messageOut += self.getDriveMotor4Data
        self.messageOut += self.getArmMotor1Data
        self.messageOut += self.getArmMotor2Data
        self.messageOut += self.getArmMotor3Data
        self.messageOut += self.getArmMotor4Data
        self.messageOut += self.getArmMotor5Data
        self.messageOut += self.getArmMotor6Data
        self.messageOut += self.getGyroscopeData
        self.messageOut += self.getBoxTempData
        self.messageOut += self.getBusMonitorData
        self.messageOut += self.getBatteryTempData
        self.messageOut += self.getVoltageConverterTempData
        self.messageOut += self.getCurrentConversionData
    
    def decomposemessageOut(self, str):
        
        #Update values of messageOut variables
        self.setErrorMessageData(str[0:1])
        self.setDriveMotor1Data(str[2:4])
        self.setDriveMotor2Data(str[5:7])
        self.setDriveMotor3Data(str[8:10])
        self.setDriveMotor4Data(str[11:13])
        self.setArmMotor1Data(str[14:18])
        self.setArmMotor2Data(str[19:23])
        self.setArmMotor3Data(str[24:28])
        self.setArmMotor4Data(str[29:33])
        self.setArmMotor5Data(str[34:38])
        self.setArmMotor6Data(str[39:43])
        self.setGyroscopeMotorData(str[44:46])
        self.setBoxTempData(str[47:49])
        self.setBusMonitorData(str[50:53])
        self.setBatteryTempData(str[54:56])
        self.setVoltageConverterTempData(str[57:59])
        self.setCurrentConversionData(str[60:63])
    
    #Checking for any errors
    def checkForError(self, str):
        #If true, no error. If false, there is an error.
        return str[0:1].lower() == "ff"
