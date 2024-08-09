import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the servo
servo_pin = 6

# Set up the servo pin as an output
GPIO.setup(servo_pin, GPIO.OUT)

# Set up PWM on the servo pin with a frequency of 50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

try:
    while True:
        # Move the servo to 0 degrees
        pwm.ChangeDutyCycle(2.5)
        time.sleep(1)
        
        # Move the servo to 90 degrees
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        
        # Move the servo to 180 degrees
        pwm.ChangeDutyCycle(12.5)
        time.sleep(1)

except KeyboardInterrupt:
    pass

# Clean up the GPIO
pwm.stop()
GPIO.cleanup()
