import time
import serial
import rospy
from std_msgs.msg import String

class Communications:

    def __init__(self,name,serialPort, baudRate=57600):

        # Initialize the Rover ROS_COMMS node
        rospy.init_node('rover_main', anonymous = True)
        

        # Subscribe to the Rover COMS_OUT topic
        rospy.Subscriber('RoverToBase', String, self.writeData)

        # initalize out internal variables and set up the publisher node and comm port!!
        self.__subscriberName = name
        self.__baudRate     = baudRate
        self.port           = serial.Serial(serialPort,self.__baudRate)           # Open the serial com port
        self.DataOutBuffer  = ""
        self.DataInBuffer   = ""
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

        pub = rospy.Publisher('BaseToRover', String, queue_size = 10)
        # Will freeze if no data is passed

        try:
            ser_bytes = self.port.read_until()
            ser_bytes = ser_bytes[:len(ser_bytes)-1]
            dataInBuffer = ser_bytes.decode()
            
            # Publish to ROS Comms In topic
            rospy.loginfo("Base to Rover:" + dataInBuffer)
            pub.publish(dataInBuffer)
            rate.sleep()
        
        except Exception as e:
            rospy.loginfo("ERROR_COMMS_IN: " + e)

     


