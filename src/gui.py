#!/usr/bin/env python3

#from multiprocessing import Process
from threading import Thread
from functools import partial
import tkinter as tk
import add_week, burn_logger
import os

class Gui:
    def __init__(self, path='me.db'):
        root = tk.Tk()
        tk.Button(root, text='Add Week', command=partial(self.add_week, path)).pack()
        tk.Button(root, text='Burn Log', command=partial(self.burn_log, path)).pack()
        root.mainloop()
    

    def add_week(self, path):
        t = Thread(target=add_week.Gui, args=(path,))
        t.start()
    

    def burn_log(self, path):
        t = Thread(target=burn_logger.Gui, args=(path,))
        t.start()


if __name__ == '__main__':
    # make sure we are in the correct directory:
    try:
        assert 'me.db' in os.listdir()
    except AssertionError as e:
        print(e)
        print('Not in same directory as "me.db"')
        exit()
    # connect to 'me.db'
    # initialize the gui:
    Gui(path='me.db')