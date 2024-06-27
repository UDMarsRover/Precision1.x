#!/usr/bin/env python3

# Composes and decomposes the messageOuts sent between rover and base
from inputs import get_gamepad
import _thread

class LogitechF310:
    def __init__(self):
        self.left_joy_x = 0.0
        self.left_joy_y = 0.0
        self.right_joy_x = 0.0
        self.right_joy_y = 0.0
        self.dpad_x = 0.0
        self.dpad_y = 0.0
        self.back = 0
        self.start = 0
        self.a = 0
        self.b = 0
        self.x = 0
        self.y = 0
        self.rb = 0
        self.lb = 0
        self.rt = 0
        self.lt = 0

        try:
            print("Starting Controller Interface Thread...")
            _thread.start_new_thread(self.update,("Hi", ))
            print("Controller Interface Thread Started!")
        except Exception as e:
            print("ERROR - Unable to start controller thread")
            print(e)
            exit()

    def update(self,__):
        while True:
            #print("Thread Updating..")
            event = get_gamepad()[0]
            if event.code == "BTN_THUMB":
                self.a = event.state
            elif event.code == "BTN_THUMB2":
                self.b = event.state
            elif event.code == "BTN_TRIGGER":
                self.x = event.state
            elif event.code == "BTN_TOP":
                self.y = event.state
            elif event.code == "ABS_RZ":
                self.left_joy_y = round((int(event.state) - 128) / -128, 1)
            elif event.code == "ABS_Z":
                self.left_joy_x = round((int(event.state) - 128) / 128, 1)
            elif event.code == "ABS_Y":
                self.right_joy_y = round((int(event.state) - 128) / -128, 1)
            elif event.code == "ABS_X":
                self.right_joy_x = round((int(event.state) - 128) / 128, 1)
            elif event.code == "ABS_HAT0X":
                self.dpad_x = event.state
            elif event.code == "ABS_HAT0Y":
                self.dpad_y = int(event.state) * -1
            elif event.code == "BTN_BASE4":
                self.start = event.state
            elif event.code == "BTN_BASE3":
                self.back = event.state
            elif event.code == "BTN_PINKIE":
                self.rb = event.state
            elif event.code == "BTN_BASE2":
                self.rt = event.state
            elif event.code == "BTN_TOP2":
                self.lb = event.state
            elif event.code == "BTN_BASE":
                self.lt = event.state
            else:
                None


class Arm_Position:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.grip = False

    def getArmCommand(self):
        return [self.x, self.y, self.z, self.roll, self.pitch, self.yaw]
    
    def nonZeros(self):
        return ((self.x != 0.0) or
                (self.y != 0.0) or
                (self.z != 0.0) or
                (self.roll != 0.0) or
                (self.pitch != 0.0) or
                (self.yaw != 0.0))


class UDMRTDataBuffer:
    def __init__(self):
        # Variables
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

    # Getter and setter methods... lots of them...

    def setErrorMessageData(self):
        # Do some logic for determining error code

        strOut = "NULL"
        self.__errorMessageData__ = strOut

    def getErrorMessageData(self):
        return self.__errorMessageData__

    def getDriveMotor1Data(self):
        return self.__driveMotor1Data__

    def getDriveMotor2Data(self):
        return self.__driveMotor2Data__

    def getDriveMotor3Data(self):
        return self.__driveMotor3Data__

    def getDriveMotor4Data(self):
        return self.__driveMotor4Data__

    def getArmMotor1Data(self):
        return self.__armMotor1Data__

    def getArmMotor2Data(self):
        return self.__armMotor2Data__

    def getArmMotor3Data(self):
        return self.__armMotor3Data__

    def getArmMotor4Data(self):
        return self.__armMotor4Data__

    def getArmMotor5Data(self):
        return self.__armMotor5Data__

    def getArmMotor6Data(self):
        return self.__armMotor6Data__

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

    def setDriveMotorData(self, dataIn):
        str = dataIn.data
        self.__driveMotorErrorData__ = str[0:2]
        self.__driveMotor1Data__ = str[2:5]
        self.__driveMotor2Data__ = str[5:8]
        self.__driveMotor3Data__ = str[8:11]
        self.__driveMotor4Data__ = str[11:14]

    def setArmMotorData(self, dataIn):
        str = dataIn.data
        self.__armMotorErrorData__ = str[0:2]
        self.__armMotor1Data__ = str[2:7]
        self.__armMotor2Data__ = str[7:12]
        self.__armMotor3Data__ = str[12:17]
        self.__armMotor4Data__ = str[17:22]
        self.__armMotor5Data__ = str[22:27]
        self.__armMotor6Data__ = str[27:32]

    def setEmoData(self, dataIn):
        str = dataIn.data
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

    # def setCameraData(self, dataIn):
    #    self.__cameraData__ = dataIn.data

    def composeMessageOut(self):
        # Concatenate all of the variables together into one __messageOut__
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

    # Checking for any errors
    def checkForError(self):
        # If true, no error. If false, there is an error.
        return self.__emoErrorData__.lower() == "ff"
