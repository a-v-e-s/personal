import tkinter as tk
import add_week, burn_logger
#from multiprocessing import Process
from threading import Thread
from functools import partial

class Gui:
    def __init__(self):
        root = tk.Tk()
        tk.Button(root, text='Add Week', command=self.add_week).pack()
        tk.Button(root, text='Burn Log', command=self.burn_log).pack()
        root.mainloop()
    

    def add_week(self):
        t = Thread(target=add_week.Gui)
        t.start()
    

    def burn_log(self):
        t = Thread(target=burn_logger.Gui)
        t.start()


if __name__ == '__main__':
    Gui()