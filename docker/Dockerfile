#! Dockerfile
#

# This file was created by Greg Molskow for the use of UDMRT club members
# The goal of this image is to create a developemnt enviornment for 
# UDMRT that already has ROS and all of the required packages installed.


######## Create the main image for the system ########
FROM ros:noetic AS rover_dev_main_v1.0

ARG branch="master"

# Install OS tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install git -y && \
    apt-get install ros-noetic-cv-bridge -y && \
    apt-get install python3-pip -y

# Install and Update Development/ROS tools
RUN pip install pyserial && \
    pip install opencv-python &&\
    rosdep update


# Install code from git and update local repo to correct branch
WORKDIR /home/udmrt

RUN mkdir /home/udmrt/precision1
RUN mkdir /home/udmrt/precision1/src

######## Create the image for the auxillary devices ######## 
FROM rover_dev_main_v1.0 AS rover_aux


######## Create the image for the host devices ########
FROM rover_dev_main_v1.0 AS rover_host