#!/bin/bash

# Source the ROS library
source /opt/ros/melodic/setup.bash

# Get the most recent version of the repo from the set branch
cd /home/udmrt/precision1
branch=cat branch.txt
git pull
git checkout $branch
git pull

cd precision1
# Build the ROS project
catkin_make

# Source the newly built project 
source ./devel/setup.bash

exec $@
