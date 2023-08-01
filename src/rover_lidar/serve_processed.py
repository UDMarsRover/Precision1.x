#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from flask import Flask, render_template

# Define a global variable to store the objects data
objects_data = None

# Define a callback function to process the objects data
def objects_callback(data):
    global objects_data
    # Split the data string into a list of objects strings
    objects_data = data.data.split("\n")

# Define a function to create a flask app and display the objects graphically
def display_objects():
    # Initialize a node for this script
    rospy.init_node('display_objects', anonymous=True)
    # Subscribe to the objects topic and register the callback function
    rospy.Subscriber('objects', String, objects_callback)
    
    # Create a flask app instance 
    app = Flask(__name__)
    
    # Define a route for the home page 
    @app.route('/')
    def index():
        # Check if there is any objects data available 
        if objects_data:
            # Initialize an empty list to store the coordinates of each object's midpoint 
            midpoints = []
            # Loop through each object string and extract its attributes 
            for obj_str in objects_data:
                # Split the object string by commas and strip any whitespace 
                obj_attr = [x.strip() for x in obj_str.split(",")]
                # Get the width, angle and distance of each object as floats 
                width = float(obj_attr[0].split()[1])
                angle = float(obj_attr[1].split()[1])
                distance = float(obj_attr[2].split()[1])
                # Calculate the x and y coordinates of each object's midpoint using polar to cartesian conversion 
                x = distance * math.cos(angle)
                y = distance * math.sin(angle)
                # Append the coordinates as a tuple to the list of midpoints 
                midpoints.append((x,y))
            
            # Render an HTML template with the midpoints data passed as an argument 
            return render_template('index.html', midpoints=midpoints)
        else:
            # Return a message indicating no data available 
            return "No objects data available."
    
    # Run the flask app on port 5000  
    app.run(port=5000)

if __name__ == '__main__':
    try:
        display_objects()
    except rospy.ROSInterruptException:
        pass
