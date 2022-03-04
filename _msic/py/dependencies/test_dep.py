from dependencies import Injector


class Robot(object):
    a = 1

    def __init__(self, environment, bbc=2):
        self.environment = environment
        print(environment, bbc)

    def work(
        self,
    ):
        print(self.environment)


class Container(Injector):
    robot = Robot
    bbc = 123
    environment = "production"


Container.robot.work()
