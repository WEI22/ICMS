import RPi.GPIO as GPIO

class Motor:

    def __init__(self, forward, backward, pwm):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([forward, backward, pwm], GPIO.OUT)

        GPIO.output(forward, GPIO.LOW)
        GPIO.output(backward, GPIO.LOW)

        self.forward = forward
        self.backward = backward
        self.pwm = GPIO.PWM(pwm, 1000)
        self.pwm.start(25)

    def run(self, direction, speed):
        if direction == "forward":
            GPIO.output(self.forward, GPIO.HIGH)
            GPIO.output(self.backward, GPIO.LOW)
            self.pwm.ChangeDutyCycle(speed)

        elif direction == "backward":
            GPIO.output(self.forward, GPIO.LOW)
            GPIO.output(self.backward, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.forward, GPIO.LOW)
        GPIO.output(self.backward, GPIO.LOW)
        self.pwm.ChangeDutyCycle(25)

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

        self.motor1 = Motor(14, 15, 18)
        self.motor2 = Motor(23, 24, 12)
        self.motor3 = Motor(17, 27, 13)
        self.motor4 = Motor(5, 6, 19)

        self.speed = 25

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()

    def forward(self, speed=25):
        self.motor1.run("forward", speed)
        self.motor2.run("forward", speed)
        self.motor3.run("forward", speed)
        self.motor4.run("forward", speed)
        self.speed = speed

    def backward(self, speed=25):
        self.motor1.run("backward", speed)
        self.motor2.run("backward", speed)
        self.motor3.run("backward", speed)
        self.motor4.run("backward", speed)
        self.speed = speed

    def left(self):
        self.motor1.run("backward", self.speed)
        self.motor2.run("backward", self.speed)
        self.motor3.run("forward", self.speed)
        self.motor4.run("forward", self.speed)

    def right(self):
        self.motor1.run("forward", self.speed)
        self.motor2.run("forward", self.speed)
        self.motor3.run("backward", self.speed)
        self.motor4.run("backward", self.speed)

