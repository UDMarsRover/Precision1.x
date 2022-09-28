#! Dockerfile
#
# This file was created by Greg Molskow for the use of UDMRT club members
# The goal of this image is to create a developemnt enviornment for 
# UDMRT that already has ROS and all of the required packages installed.

FROM ros:noetic AS presision1


# Define the gitHub branch to pull from.
ARG branch="Greg"

# Install OS tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install git -y && \
    apt-get install python3-pip -y

# Install and Update Development/ROS tools
RUN pip install pyserial && \
    rosdep update

# Create a user and usergroup for club
RUN groupadd udmrt && \
    useradd -m udmrt -g udmrt


# Install code from git and update local repo to correct branch
WORKDIR /home/udmrt
RUN git clone https://github.com/UDMarsRover/precision1.git && \
    cd precision1 && \
    git pull && \
    git checkout $branch &&\
    git pull


# Build ROS project from branch
RUN /bin/bash -c    "source /opt/ros/noetic/setup.bash && \
                    cd /home/udmrt/precision1 && \
                    catkin_make && \
                    source ./devel/setup.bash"

# Update ownership for files in the udmrt home dir
RUN chown -R udmrt /home/udmrt && \
    chmod g+rw -R /home/udmrt

# Switch user to udmrt user to insure no root access is given
USER udmrt
