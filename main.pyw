from multiprocessing import Process, Manager
# from CanvasOCV import CanvasOCV
from threading import Thread
from tkinter import *
from time import sleep

class My(Tk):
    def __init__(self, shared, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('600x400')
        self.shared = shared
        self.labelVar = IntVar(0)
        self.label = Label(textvariable=(self.labelVar))
        self.label.pack(fill=BOTH, expand = 1)
        self.label.bind('<Button-1>', self.click)
        self.loopThread = Thread(name='mainloop', target=self.loop, daemon=True)
        self.loopThread.start()

    def click(self, event):
        self.shared[0] += 1
        self.labelVar.set(self.shared[0])

    def loop(self):
        "Is running in separate thread."
        while True:
            self.labelVar.set(self.shared[0])
            sleep(0.05)

def mainloop(d, l):
    root = My(l)
    root.mainloop()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list([0])
        p = []
        for i in range(2):
            p.append(Process(target=mainloop, args=(d, l)))
        for i in range(2):
            p[i].start()
        for i in range(2):
            p[i].join()