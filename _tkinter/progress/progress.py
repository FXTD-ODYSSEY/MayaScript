# -*- coding: utf-8 -*-
"""
进度条
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-09 22:41:49'


import threading

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog, messagebox
except:
    import ttk
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

def take_parm(kwargs,key,default = None):
    res = kwargs.get(key,default)
    if key in kwargs:
        del kwargs[key]
    return res

class ProgressDialog(tk.Toplevel):

    canceled = False

    def __init__(self, *args, **kwargs):
        self.parent = take_parm(kwargs,'parent')
        tk.Toplevel.__init__(self, self.parent,*args, **kwargs)

        # NOTE 阻断其他窗口
        self.grab_set()
        self.progress = ttk.Progressbar(self, orient = tk.HORIZONTAL, 
			length = 100, mode = 'determinate') 
        self.progress.pack(side="top", fill="x", expand=1, padx=5,pady=5) 
        self.button = tk.Button(self,text="Cancel", command=lambda:[None for self.canceled in [True]])
        self.button.pack()

    @classmethod
    def loop(cls,seq,**kwargs):
        self = cls(**kwargs)
        maximum = len(seq)
        for i,item in enumerate(seq):
            if self.canceled:break
            
            try:
                yield item  # with body executes here
            except:
                import traceback
                traceback.print_exc()
                self.destroy()
            
            self.progress['value'] = i/maximum * 100
            self.update()
        
        self.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    tk.Button(root, text = 'Start', command = lambda : [i for i in ProgressDialog.loop(range(9900))]).pack(pady = 10) 
    root.mainloop()