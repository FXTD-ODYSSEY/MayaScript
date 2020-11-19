class ProgressDialog(tk.Toplevel):

    canceled = False

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent',None)
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
                yield i,item  # with body executes here
            except:
                import traceback
                traceback.print_exc()
                self.destroy()
            
            self.progress['value'] = i/maximum * 100
            self.update()
        
        self.destroy()