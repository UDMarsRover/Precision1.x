import time
import serial
import rospy
from std_msgs.msg import String as rosstring

class Communications:

    def __init__(self,name, pullTopic, pushTopic, serialPort, baudRate=57600):
        # initalize out internal variables and set up the publisher node and comm port!!
        self.__subscriberName = name
        self.__baudRate = baudRate
        self.__pushTopic = pushTopic                                    # Save the topic to subscribe to  for debugging
        self.__pullTopic = pullTopic
        self.port = serial.Serial(serialPort,self.__baudRate)           # Open the serial com port
        self.__pub = rospy.Publisher(self.__pullTopic, rosstring, queue_size=10)
        rospy.init_node(name)
    
    # Private function used to take in published data and write it over the comms
    def __callback(self, dataIn):
        message = dataIn.data                           # Take in published data from the topic
        rospy.loginfo(self.__subscriberName + message)  # Create an entry in the log for debugging
        self.port.write(bytes(message,'utf-8'))               # Write the data to the comms device
        self.port.write(bytes('\n','utf-8'))                  # Write our termination value to indicate the message is over
        print("Send Stuff Yo")
         
    # Getter function for getting baud rate
    def getBaud(self):
        return self.__baudRate
    
    # Send data out
    def pushCheck(self):
        rospy.Subscriber(self.__pushTopic, rosstring, self.__callback)    # Listen to Topic

    # Check to see if there is data that was sent to the reciver
    def pullCheck(self):
        # Com port input here!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rospy.loginfo("Test Output Log")
        self.__pub.publish(ser_bytes)


