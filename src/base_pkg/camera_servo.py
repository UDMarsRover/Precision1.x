import time

import RPi.GPIO as gpio

class ServoController:
    def __init__(self, pin):
        self.servo_pin = 6
        gpio.setmode(gpio.BCM)
        gpio.setup(self.servo_pin, gpio.OUT)
        self.p = gpio.PWM(self.servo_pin, 250)
        self.p.start(0) # duty cycle 2.5%

    def set_angle(self, angle):
        setting = 35 + angle * (25 / 90.0)
        self.p.ChangeDutyCycle(setting)

    

    def cleanup(self):
        self.p.stop()
        gpio.cleanup()

if __name__ == "__main__":
    servo = ServoController(17)

    try:
        while True:
            angle = float(input("Enter angle (-100 - 100): "))
            servo.set_angle(angle)
    except KeyboardInterrupt:
        servo.cleanup()
