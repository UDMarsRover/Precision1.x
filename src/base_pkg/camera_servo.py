import time

import RPi.GPIO as gpio

class ServoController:
    def __init__(self, pin):
        self.servo_pin = 17
        gpio.setmode(gpio.BCM)
        gpio.setup(self.servo_pin, gpio.OUT)
        self.p = gpio.PWM(self.servo_pin, 50)
        self.p.start(0) # duty cycle 2.5%

    def set_angle(self, angle):
        duty_cycle = angle / 18 + 2
        self.p.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        gpio.cleanup()

if __name__ == "__main__":
    servo = ServoController(17)

    try:
        while True:
            angle = float(input("Enter angle (0-360): "))
            servo.set_angle(angle)
    except KeyboardInterrupt:
        servo.cleanup()