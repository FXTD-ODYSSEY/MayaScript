# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-09 22:22:12'

import os
import time
import Queue
import threading
from Tkinter import *
import ttk

class GUI:
    def __init__(self, master):
        self.master = master
        self.test_button = Button(self.master, command=self.tb_click)
        self.test_button.configure(
            text="Start", background="Grey",
            padx=50
            )
        self.test_button.pack(side=TOP)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self.master, orient="horizontal",
            length=200, mode="determinate"
            )
        self.prog_bar.pack(side=TOP)

    def tb_click(self):
        self.progress()
        self.prog_bar.start()
        self.queue = Queue.Queue()
        ThreadedTask(self.queue,self.prog_bar).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            self.prog_bar.stop()
        except Queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    
    def __init__(self, queue,progress):
        threading.Thread.__init__(self)
        self.queue = queue
        self.progress = progress

    def run(self):
        # self.progress['value'] = 10
        time.sleep(1)  # Simulate long running process
        self.queue.put("Task finished")

root = Tk()
root.title("Test Button")
main_ui = GUI(root)
root.mainloop()