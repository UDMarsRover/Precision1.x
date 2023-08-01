#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray
import numpy as np

pub = rospy.Publisher('Lidar_Processed', Float32MultiArray, queue_size=10)


def callback(msg):
    import numpy as np
    from scipy.ndimage import gaussian_filter

    # Assume your lidar scan array is stored in a variable called scan
    scan = np.array(msg.ranges) # 760 values representing the distances at angles

    # Apply a gaussian filter with a sigma value of your choice (e.g. 0.5)
    filtered_scan = gaussian_filter(scan, sigma=0.5)

    # Print or plot the filtered scan array
    print(find_closest_objects(filtered_scan))

# Define a function to find the 5 closest objects in the scan array
def find_closest_objects(scan):
    # Initialize an empty list to store the objects data
    objects = []
    # Loop through each value in the scan array
    for i in range(len(scan)):
        # Get the distance and angle of the current value
        distance = scan[i]
        angle = i * np.pi / 380 # Assuming 760 values cover 180 degrees
        # Check if the current value is smaller than a threshold (e.g. 10)
        if distance < 10:
            # Check if there is already an object in the list
            if objects:
                # Get the last object in the list
                last_object = objects[-1]
                # Check if the current value is close enough to the last object (e.g. within 5 degrees)
                if abs(angle - last_object["end_angle"]) < np.pi / 36:
                    # Update the last object's end angle and width
                    last_object["end_angle"] = angle
                    last_object["width"] = distance * (last_object["end_angle"] - last_object["start_angle"])
                else:
                    # Create a new object with start angle, end angle and width attributes
                    new_object = {"start_angle": angle, "end_angle": angle, "width": 0}
                    # Append the new object to the list of objects
                    objects.append(new_object)
            else:
                # Create a new object with start angle, end angle and width attributes
                new_object = {"start_angle": angle, "end_angle": angle, "width": 0}
                # Append the new object to the list of objects
                objects.append(new_object)
    
    # Sort the list of objects by their distance (ascending order)
    objects.sort(key=lambda obj: scan[int(obj["start_angle"] * 380 / np.pi)])
    
    # Return only the first 5 objects in the list 
    return objects[:5]



rospy.init_node('processed_scan')
sub = rospy.Subscriber('scan', LaserScan, callback)
rospy.spin()