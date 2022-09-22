#!/bin/bash

source /opt/ros/melodic/setup.bash

cd /home/udmrt/precision1

catkin_make

source ./devel/setup.bash

roscore