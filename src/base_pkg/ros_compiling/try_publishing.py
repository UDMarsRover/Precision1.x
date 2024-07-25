#!/usr/bin/env python3
# ^ Always put this in the first line so the interpereter knows where to find python.

import rospy
from std_msgs.msg import Float32MultiArray 
import random

# We use classes so this can just be imported and run by a main python script.
class FloatArrayPublisher():
    def __init__(self):
        None # Class Initialization
        # create publisher, initialize, set rate.

    def publish():
        None # Write loop to publish
        # Create the random array
        random_array = [random.uniform(0.0, 1.0) for _ in range(10)]
        # You will have to create a Float32MultiArray (Hint: use constructor, data=random_array)


    
