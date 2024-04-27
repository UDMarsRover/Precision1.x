#!/usr/bin/env python3
from std_msgs.msg import String
from rover import Rover

# The main Loop
if __name__ == "__main__":
    p1 = Rover()
    # Run Forever
    while not p1.kill:
        p1.spin()
    p1.led_control(0,1,1)
    print("KILLED")
    #p1.shutdown()
