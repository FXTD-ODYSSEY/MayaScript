from blinker import signal
from blinker import Signal

s = Signal()
# q = signal('queue')


@s.connect
def animal(a,sender,b):
    print(sender,b)
    print('我是小钻风，大王回来了，我要去巡山')
    return 1


@s.connect
def animal2(a,sender,b):
    print(sender,b)
    print('我是小钻风22，大王回来了，我要去巡山')
    return 2



if "__main__" == __name__:

    res = s.send(1,b=12,sender=123)
    print(res)
    res = s.receivers
    print(res)
    # if res:
    #     s.send()

    # res = q.receivers
    # print(res)
    # if res:
    #     q.send()
    # else:
    #     print("孩儿们都出去巡山了")