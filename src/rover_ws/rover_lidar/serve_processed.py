#!/usr/bin/env python3

import rospy
from object_msgs.msg import ObjectArray
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io

# create a flask app
app = Flask(__name__)

# create a global variable to store the objects from the ros topic
objects = None

# create a callback function to update the objects variable
def object_callback(msg):
    global objects
    objects = msg.objects

# create a subscriber to the /objects topic
object_sub = rospy.Subscriber("/objects", ObjectArray, object_callback)

# create a route for the web page
@app.route("/")
def index():
    # check if there are any objects received
    if objects is not None:
        # create a figure with matplotlib
        fig = plt.figure()
        # plot the angle and distance of each object as a scatter plot
        plt.scatter([obj.angle for obj in objects], [obj.distance for obj in objects])
        # label the axes and title
        plt.xlabel("Angle (rad)")
        plt.ylabel("Distance (m)")
        plt.title("Objects detected by lidar")
        # save the figure to an in-memory buffer as png format
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        # encode the buffer as base64 string
        data = buf.getvalue().encode("base64")
    else:
        # set data to None if no objects received yet
        data = None
    
    # render the web page with flask using index.html template and pass data as argument 
    return render_template("index.html", data=data)

if __name__ == "__main__":
    # initialize a node 
    rospy.init_node("web_display")
    # run the flask app on port 5000 
    app.run(port=5000)