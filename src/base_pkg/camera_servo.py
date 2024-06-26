import time

import RPi.GPIO as GPIO

class ServoController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = angle / 18 + 2
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = ServoController(18)

    try:
        while True:
            angle = float(input("Enter angle (0-360): "))
            servo.set_angle(angle)
    except KeyboardInterrupt:
        servo.cleanup()