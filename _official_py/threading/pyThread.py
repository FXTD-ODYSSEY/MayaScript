import threading
import time

import Queue

#somewhere accessible to both:
callback_queue = Queue.Queue()

def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False) #doesn't block
        except Queue.Empty: #raised when queue is empty
            break
        callback()

def print_num(dummyid, n):
    print "From %s: %d" % (dummyid, n)

def dummy_run(dummyid):
    for i in xrange(5):
        from_dummy_thread(lambda: print_num(dummyid, i))
        time.sleep(0.5)

threading.Thread(target=dummy_run, args=("a",)).start()
threading.Thread(target=dummy_run, args=("b",)).start()


while True:
    from_main_thread_blocking()
print "test"