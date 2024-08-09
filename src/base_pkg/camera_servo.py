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
        # duty_cycle = 34.6 + angle / 50.0
        # duty_cycle = angle
        if angle > 100:
            self.p.ChangeFrequency(50)
            self.p.ChangeDutyCycle(12.5)
            time.sleep(0.001)
            self.p.ChangeDutyCycle(0)
        else:
            self.p.ChangeFrequency(250)
            self.p.ChangeDutyCycle(angle)
        time.sleep(0.5)

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
