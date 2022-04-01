from dependencies import Injector
import attr

@attr.s
class Robot(object):
    bbc = attr.ib()
    test = attr.ib()

    def work(self):
        print("work Robot")
        
@attr.s
class Timer(object):
    robot = attr.ib()
    def work(self):
        print("work Timer")
        print(self.robot.work())
    

class Container(Injector):
    robot = Robot
    timer = Timer
    bbc = 123
    environment = "production"

    def test():
        print(Container.robot.work)

Container.timer.work()
