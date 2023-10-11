from time import sleep
import RPi.GPIO as GPIO


class Servo:
    def __init__(self, config):
        """
        Create a servo.
        :param config: configuration of the servo.
        """
        GPIO.setup(config.gpio, GPIO.OUT)
        self.config = config
        self.angle = 0

    def set_angle(self, angle):
        """
        Set the angle of the servo from an angle.
        :param angle: angle in deg.
        :return:
        """
        pwm = GPIO.PWM(self.config.gpio, 50)
        pwm.start(8)
        duty_cycle = angle / 18. + 3.
        pwm.ChangeDutyCycle(duty_cycle)
        sleep(0.3)
        pwm.stop()

    def set_angle_from_coord(self, x):
        """
        Set the angle of the servo from a coordinate.
        :param x: coordinate in pixels.
        :return:
        """
        if x < self.config.centered_min:
            self.angle += self.config.servo_step
            if self.angle > self.config.servo_max:
                self.angle = self.config.servo_max
            self.set_angle(self.angle)

        if x > self.config.centered_max:
            self.angle -= self.config.servo_step
            if self.angle < self.config.servo_min:
                self.angle = self.config.servo_min
            self.set_angle(self.angle)


class PanTilt:
    def __init__(self, pan_config, tilt_config):
        """
        Create Pan Tilt mechanism controller.
        :param pan_config: configuration of the pan motor.
        :param tilt_config: configuration of the tilt motor.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pan = Servo(pan_config)
        self.tilt = Servo(tilt_config)

    def set_state_from_object(self, x, y):
        """
        Set PanTilt state from object center on image.
        :param x: x-coordinate of object in image.
        :param y: y-coordinate of object in image.
        :return:
        """
        self.pan.set_angle_from_coord(x)
        self.tilt.set_angle_from_coord(y)
