# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/22113207/keep-tkinter-progressbar-running-until-a-file-is-created
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-09 22:17:01'

import os
from Tkinter import *
import ttk

class UI(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.master = master
        self.initUI()

    def initUI(self):
        self.popup = popup = Toplevel(self)
        Label(popup, text="Please wait until the file is created").grid(
            row=0, column=0)
        self.progressbar = progressbar = ttk.Progressbar(popup,
            orient=HORIZONTAL, length=200, mode='indeterminate')
        progressbar.grid(row=1, column=0)
        progressbar.start()
        self.checkfile()

    def checkfile(self):
        if os.path.exists("myfile.txt"):
            print ('found it')
            self.progressbar.stop()
            self.popup.destroy()
        else:
            print ('not created yet')
            self.after(100, self.checkfile) # Call this method after 100 ms.

if __name__ == "__main__":
    root = Tk()
    aplicacion = UI(root)
    root.mainloop()