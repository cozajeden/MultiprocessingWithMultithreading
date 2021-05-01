import multiprocessing as mp
from threading import Thread
from tkinter import *



class My(Tk):
    def __init__(self, shared, clickEvent, destroyEvent, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('600x400')
        self.shared = shared
        self.clickEvent = clickEvent
        self.destroyEvent = destroyEvent
        self.index = index
        self.labelVar = IntVar(0)
        self.label = Label(textvariable=(self.labelVar))
        self.label.pack(fill=BOTH, expand = 1)
        self.label.bind('<Button-1>', self.click)
        self.loopThread = Thread(name='mainloop', target=self.loop, args=(shared, clickEvent,), daemon=True)
        self.loopThread.start()
        self.destroyThread = Thread(name='destroy', target=self.destroy_lisener, args=(destroyEvent,), daemon=True)
        self.destroyThread.start()

    def click(self, event):
        self.shared[0] += 1
        self.shared[1:2] = [1, 1]
        self.labelVar.set(self.shared[0])
        self.clickEvent.set()

    def loop(self, shared, clickEvent):
        "Is running in separate thread."
        while True:
            clickEvent.wait()
            print(f'clickEvent occurred in process with index {self.index}')
            self.labelVar.set(shared[0])
            if shared[self.index]:
                shared[self.index] = 0
                if not sum(shared[1:2]):
                    clickEvent.clear()

    def destroy_lisener(self, destroyEvent):
        destroyEvent.wait()
        print(f'destroyEvent occurred in process with index {self.index}')
        self.destroy()

    def destroy(self):
        self.shared[3] = 1
        self.destroyEvent.set()
        super().destroy()
            

def mainloop(d, l, e1, e2, i):
    root = My(l, e1, e2, i)
    root.mainloop()

if __name__ == '__main__':
    # mp.freeze_support() # Uncomment this if you want to use pyinstaller
    with mp.Manager() as manager:
        d = manager.dict()
        l = manager.list([0, 0, 0, 0])
        e1 = mp.Event()
        e2 = mp.Event()
        p = []
        for i in range(1):
            p.append(mp.Process(target=mainloop, args=(d, l, e1, e2, 1)))
            p.append(mp.Process(target=mainloop, args=(d, l, e1, e2, 2)))
        for i in range(2):
            p[i].start()
        for i in range(2):
            p[i].join()