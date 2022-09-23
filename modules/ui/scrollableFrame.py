from tkinter import *

class ScrollableFrame:
    def __init__(self, master, bg='#ffffff', x=0, y=0, width=0, height=0):
        self.masterFrame = Frame(master, highlightthickness=0, bg=bg)
        self.masterFrame.place(x=x, y=y)
        self.canvas = Canvas(self.masterFrame, bg=bg, width=width, height=height, highlightthickness=0)
        self.scrollbar = Scrollbar(self.masterFrame, orient='vertical', command=self.canvas.yview)
        self.scrollableFrame = Frame(self.canvas, bg=bg)
        self.scrollableFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
    def place(self, x, y):
        #self.masterFrame.place(x=x, y=y)
        self.canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        self.scrollbar.pack(side="right", fill="y")
        
    def clear(self):
        for widget in self.scrollableFrame.winfo_children():
            widget.destroy()