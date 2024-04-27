#!/usr/bin/env python3
from std_msgs.msg import String
from rover import Rover
import time

# The main Loop
if __name__ == "__main__":
    p1 = Rover()
    # Run when rover is not requested to die
    start = time.time()
    killCount = 0
    while killCount < 5:
        p1.spin()
        currTime = time.time()
        if p1.kill and (currTime - start > 1):
            killCount += 1
            start = currTime
        
        if not p1.kill: killCount = 0
    p1.log("Rover Killed")
    p1.led_control(0,1,1)
    print("KILLED")
    p1.shutdown()
