import RPi.GPIO as GPIO
import time
import sys

class Motor:

    def __init__(self, forward, backward):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([forward, backward], GPIO.OUT)

        GPIO.output(forward, GPIO.LOW)
        GPIO.output(backward, GPIO.LOW)

        self.forward = forward
        self.backward = backward

    def run(self, direction):
        if direction == "forward":
            GPIO.output(self.forward, GPIO.HIGH)
            GPIO.output(self.backward, GPIO.LOW)

        elif direction == "backward":
            GPIO.output(self.forward, GPIO.LOW)
            GPIO.output(self.backward, GPIO.HIGH)
 
    def stop(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.LOW)

class RobotCar:
    """
    front left  motor = 14, 15, 18(pwm0) - motor 1
    back left motor = 23, 24, 12(pwm0) - motor 2
    front right motor = 17, 27, 13(pwm1) - motor 3
    back right motor = 5, 6, 19(pwm1) - motor 4
    """

    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.motor1 = Motor(14, 15)
        self.motor2 = Motor(23, 24)
        self.motor3 = Motor(17, 27)
        self.motor4 = Motor(5, 6)

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def forward(self):
        self.motor1.run("forward")
        self.motor2.run("forward")
        self.motor3.run("forward")
        self.motor4.run("forward")

    def backward(self):
        self.motor1.run("backward")
        self.motor2.run("backward")
        self.motor3.run("backward")
        self.motor4.run("backward")

    def left(self):
        self.motor1.run("backward")
        self.motor2.run("backward")
        self.motor3.run("forward")
        self.motor4.run("forward")

    def right(self):
        self.motor1.run("forward")
        self.motor2.run("forward")
        self.motor3.run("backward")
        self.motor4.run("backward")

    def __del__(self):
        del self.motor1
        del self.motor2
        del self.motor3
        del self.motor4
        GPIO.cleanup()

if __name__ == "__main__":
    if sys.argv[1] == "servo":

        servo_pin = int(sys.argv[2])
        val = float(sys.argv[3])

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(servo_pin, GPIO.OUT)

        servo = GPIO.PWM(servo_pin, 50)
        servo.start(val)
        time.sleep(0.2)
        GPIO.cleanup()
        del servo

    elif sys.argv[1] == "motor":
        r = RobotCar()
        if sys.argv[2] == "forward":
            r.forward()
        elif sys.argv[2] == "backward":
            r.backward()
        elif sys.argv[2] == "left":
            r.left()
        elif sys.argv[2] == "right":
            r.right()
        elif sys.argv[2] == "stop":
            r.stop()
        del r
