import RPi.GPIO as GPIO
import time
from rplidar import RPLidar
import math

# Pin setup for L298N motor driver
LEFT_MOTOR = 17
RIGHT_MOTOR = 18
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup([LEFT_MOTOR, RIGHT_MOTOR, ULTRASONIC_TRIG], GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO, GPIO.IN)

def get_distance():
    GPIO.output(ULTRASONIC_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIG, False)
    
    start_time = time.time()
    while GPIO.input(ULTRASONIC_ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ULTRASONIC_ECHO) == 1:
        end_time = time.time()
    
    duration = end_time - start_time
    distance = (duration * 34300) / 2  # Speed of sound in cm/s
    return distance

def move_forward():
    GPIO.output(LEFT_MOTOR, True)
    GPIO.output(RIGHT_MOTOR, True)

def stop():
    GPIO.output(LEFT_MOTOR, False)
    GPIO.output(RIGHT_MOTOR, False)

def main():
    lidar = RPLidar('/dev/ttyUSB0')  # Adjust port as needed
    try:
        for scan in lidar.iter_scans():
            distance = get_distance()
            if distance < 30:  # Obstacle within 30 cm
                stop()
                print("Obstacle detected, stopping...")
            else:
                move_forward()
                print("Moving forward...")
            time.sleep(0.1)
    finally:
        lidar.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()