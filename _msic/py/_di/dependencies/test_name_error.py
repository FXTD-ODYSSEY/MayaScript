from dependencies import Injector

def create_container(data):
    class MyContainer(Injector):
        data2 = data
    return MyContainer

create_container(1)