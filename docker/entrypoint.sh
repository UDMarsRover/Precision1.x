#!/bin/bash

# Source the ROS library
source /opt/ros/melodic/setup.bash

# Get the most recent version of the repo from the set branch
cd /home/udmrt/
branch=cat branch.txt
git clone https://github.com/UDMarsRover/precision1.git
git checkout $branch
git pull

cd precision1
# Build the ROS project
catkin_make

# Source the newly built project 
source ./devel/setup.bash

exec $@
