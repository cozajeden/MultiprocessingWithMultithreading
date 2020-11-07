from multiprocessing import Process, Pipe
import multiprocessing as mp
from threading import Thread
from tkinter import *
from time import sleep

class My(Tk):
    def __init__(self, event, pipe, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('600x400')
        self.event = event
        self.pipe = pipe
        self.index = index
        self.labelVar = IntVar(0)
        self.label = Label(textvariable=(self.labelVar))
        self.label.pack(fill=BOTH, expand = 1)
        self.label.bind('<Button-1>', self.click)
        self.loopThread = Thread(name='mainloop', target=self.loop, args=(pipe,), daemon=True)
        self.loopThread.start()
        self.destroyThread = Thread(name='destroy', target=self.destroy_lisener, args=(event,), daemon=True)
        self.destroyThread.start()

    def click(self, event):
        self.labelVar.set(self.labelVar.get() + 1)
        self.pipe.send(self.labelVar.get())
        print(f'process {self.index} sent data {self.labelVar.get()} into pipeline.')

    def loop(self, pipe):
        "Is running in separate thread."
        while True:
            value = pipe.recv()
            print(f'process {self.index} recived data {value} from pipeline.')
            self.labelVar.set(value)

    def destroy_lisener(self, event):
        event.wait()
        print(f'event occurred in process with index {self.index}')
        self.destroy()

    def destroy(self):
        self.event.set()
        super().destroy()
            

def mainloop(e, p, i):
    root = My(e, p, i)
    root.mainloop()

if __name__ == '__main__':
    e = mp.Event()
    p1, p2 = mp.Pipe()
    p = [
        Process(target=mainloop, args=(e, p1, 1)),
        Process(target=mainloop, args=(e, p2, 2))
    ]
    for i in range(2):
        p[i].start()
    for i in range(2):
        p[i].join()