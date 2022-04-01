from dependencies import Injector
import attr


@attr.s
class Robot(object):
    finger_num = attr.ib(default=10)

    def create(self):
        self.create_robot_hand()

    def create_robot_hand(self):
        self.create_robot_finger()

    def create_robot_finger(self):
        print("create_robot_finger finder_number:{0}".format(self.finger_num))

class Container(Injector):
    finger_num = 10
    robot = Robot


Container.robot.create()
