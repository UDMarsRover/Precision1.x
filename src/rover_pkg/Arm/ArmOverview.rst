============
Arm Overview
============


General
=======

Connection
----------
Over hotspot:
    ip address: 10.10.10.10
    network name: NiryoRobot xx-xx-xx 
    network password: niryorobot 

Axes
----
forward: postive x
backward: negative x
left: postive y
right: negative y
up: positive z
down: negative z

ROS setup
---------
source devel/setup.bash
rosrun <pkg_name> <file_name>

ROS timeout exception is sometimes thrown (20-30% of the time) on startup, possibly
because arm does not get shutdown correctly when program ends. Using time.sleep might 
be slightly helping by giving arm more time to start before first command 


Scripts
=======

arm_main
--------
This file is the receiver that gets commands and moves the arm through pyniryo2 library

Publishes the pose values and joint values of the arm as a JointTrajectoryPoint,
command to jog pose is Float32MultiArray

Make sure that a jog pose message is published (make controller input) or an exception
will be thrown because the subscriber receives an empty value that the arm tries to 
jog pose

niryo_listener
--------------
Gets input from the controller using get_gamepad from the inputs library

Publishes the jog command to 'control_command', will only publish a message when controller input
is changed. Must use third file to continously publish the command message while an input is held 
down. Each input to controller is registered as 2 presses. 

Joint state is received from arm to update controls after base rotation passes certain threshold
(i.e. holding right will continue to move robot right instead of stopping at minimum y value)

Also publishes command to move arm to home pose and close/open gripper

Controls:
    Right: d-pad right
    Left: d-pad left
    Forward: d-pad up
    Back: d-pad down
    Up: y
    Down: a
    Positive roll: rb
    Negative roll: -
    Positive pitch: lb
    Negative pitch: -
    Positive yaw: rt
    Negative yaw: -
    Close gripper: b - release to open
    Change speed/jog distance: lt  
        3 values: 0.02, 0.01, 0.005
        Starts at 0.02, moves to next with each press
    Reset to home pose: back

publish_command
---------------
receives jog pose command from controller ('control_command' topic) and continously
publishes them to 'command' topic for arm_main to read

time.sleep is used to moderate speed that message is published so arm can receive 
each new command with little delay
