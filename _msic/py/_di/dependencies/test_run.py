from dependencies import Injector
import attr


@attr.s
class Robot(object):
    servo = attr.ib()
    controller = attr.ib()
    settings = attr.ib()
    run = attr.ib()

    def run(self, threshold=3):
        print(threshold)
        print(self.controller.di_environment)
        print(self.settings.threshold)
        print(self.servo.threshold)
        print("test")


@attr.s
class Servo(object):
    threshold = attr.ib()


@attr.s
class Amplifier(object):
    threshold = attr.ib()


@attr.s
class Controller(object):
    di_environment = attr.ib()


@attr.s
class Settings(object):
    threshold = attr.ib()


@attr.s
class Caller(object):
    threshold = attr.ib()

    def __call__(self):
        print(self.threshold)


class Container(Injector):
    threshold = 1
    caller = Caller

    robot = Robot
    servo = Servo
    amplifier = Amplifier
    controller = Controller
    settings = Settings
    di_environment = "production"


Container.robot.run()
Container.caller()
