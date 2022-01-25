from blinker import signal

s = signal('king')
q = signal('queue')


def animal(sender):
    print('我是小钻风，大王回来了，我要去巡山')

s.connect(animal)


if "__main__" == __name__:

    res = s.receivers
    print(res)
    if res:
        s.send()

    res = q.receivers
    print(res)
    if res:
        q.send()
    else:
        print("孩儿们都出去巡山了")