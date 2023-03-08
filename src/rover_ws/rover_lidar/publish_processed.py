#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

# Define a global variable to store the filtered scan data
filtered_scan = None

# Define a callback function to process the scan data
def scan_callback(data):
    global filtered_scan
    # Filter out any invalid or noisy readings from the scan data
    filtered_scan = [x for x in data.ranges if x > data.range_min and x < data.range_max]
    # Sort the filtered scan data in ascending order of distance
    filtered_scan.sort()
    
# Define a function to find the objects in the scan data and publish them to a new topic
def find_objects():
    # Initialize a node for this script
    rospy.init_node('find_objects', anonymous=True)
    # Subscribe to the scan topic and register the callback function
    rospy.Subscriber('scan', LaserScan, scan_callback)
    # Create a publisher for the new topic that will publish the objects as strings
    pub = rospy.Publisher('objects', String, queue_size=10)
    # Set the rate of publishing to 10 Hz
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        # Check if there is any filtered scan data available
        if filtered_scan:
            # Initialize an empty list to store the objects as strings
            objects = []
            # Initialize variables to keep track of the current object's width, angle and distance 
            width = 0.0 
            angle = 0.0 
            distance = 0.0 
            # Loop through the filtered scan data and find the objects based on changes in distance 
            for i in range(len(filtered_scan) - 1):
                # Calculate the difference between two consecutive readings 
                diff = abs(filtered_scan[i] - filtered_scan[i+1])
                # If the difference is larger than a threshold (e.g. 0.1 m), assume that it is a boundary between two objects 
                if diff > 0.1:
                    # Calculate the width of the current object as half of its arc length 
                    width = (i + 1) * diff / 2.0 
                    # Calculate the angle of the current object as half of its span angle 
                    angle = (i + 1) * data.angle_increment / 2.0 
                    # Calculate the distance of the current object as its average reading 
                    distance = sum(filtered_scan[:i+1]) / (i + 1) 
                    # Format the object's attributes as a string and append it to the list of objects 
                    obj_str = "Width: {:.2f} m, Angle: {:.2f} rad, Distance: {:.2f} m".format(width, angle, distance)
                    objects.append(obj_str)
                    # Reset the variables for tracking attributes for next object  
                    width = 0.0  
                    angle = 0.0  
                    distance = 0.0  
                else:
                    continue
            
            # Publish only up to five closest objects from sorted list  
            pub.publish("\n".join(objects[:5]))
        
        rate.sleep()

if __name__ == '__main__':
    try:
        find_objects()
    except rospy.ROSInterruptException:
        pass