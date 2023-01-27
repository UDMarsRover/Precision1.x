import time
import serial
import rospy
from std_msgs.msg import String

class Communications:

    def __init__(self,serialPort,pushTopic, pullTopic, baudRate=57600):

        # initalize out internal variables and set up the publisher node and comm port!!
        self.__baudRate     = baudRate
        self.__pushTopic    = pushTopic
        self.__pullTopic    = pullTopic
        self.port           = serial.Serial(serialPort,self.__baudRate)           # Open the serial com port
        self.DataOutBuffer  = ""
        self.DataInBuffer   = ""

        # Subscribe to the Rover COMS_OUT topic
        rospy.Subscriber(self.__pushTopic, String, self.writeData)
    # Getter function for getting baud rate
    def getBaud(self):
        return self.__baudRate
    
    # Send data out
    def writeData(self, dataIn):
        dataOut = dataIn.data
        try:
            for i in range(0,len(dataOut)):
                self.port.write(bytes(dataOut[i],'utf-8'))         # Write the data to the comms device
            
            self.port.write(bytes('\n','utf-8'))            # Write our termination value to indicate the message is over
        except Exception as e:
            rospy.loginfo("ERROR_COMMS_OUT: " + e)
        
        

    # Check to see if there is data that was sent to the receiver
    def readData(self):

        pub = rospy.Publisher(self.__pullTopic, String, queue_size = 10)
        # Will freeze if no data is passed

        try:
            ser_bytes = self.port.read_until()
            ser_bytes = ser_bytes[:len(ser_bytes)-1]
            dataInBuffer = ser_bytes.decode()
            
            # Publish to ROS Comms In topic to trigger the command in function
            rospy.loginfo("Base to Rover:" + dataInBuffer)
            pub.publish(dataInBuffer)
            return True
        
        except Exception as e:
            rospy.loginfo("ERROR_COMMS_IN: " + e)
            return False

     


