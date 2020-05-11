#!/usr/bin/env python3

import tkinter as tk
from datetime import date
from functools import partial
from sqlite3 import Connection

class Gui:
    def __init__(self):
        root = tk.Tk()
        root.title('Burn Log')
        r_width = str(root.winfo_screenwidth())
        r_height = str(root.winfo_screenheight() - 100)
        root.geometry(r_width + 'x' + r_height)
        #
        today = date.today().__str__()
        tk.Label(root, text='Burn Log').grid(row=1, column=1, columnspan=2)
        tk.Label(root, text='Date: ' + today).grid(row=1, column=3, columnspan=2)
        tk.Label(root, text='Description of Event:').grid(row=2, column=1, columnspan=4)
        t_width = int(r_width) // 8
        description = tk.Text(root, bg='white', width=t_width, height=4)
        description.grid(row=3, column=1, columnspan=4)
        tk.Label(root, text='Trigger Thoughts ("Shoulds" and Blamers, separated by "|"):').grid(row=4, column=1, columnspan=4)
        triggers = tk.Text(root, bg='white', width=t_width, height=4)
        triggers.grid(row=5, column=1, columnspan=4)
        tk.Label(root, text='Pre-existing stressors (separated by "|"):').grid(row=6, column=1, columnspan=4)
        stressors = tk.Text(root, bg='white', width=t_width, height=4)
        stressors.grid(row=7, column=1, columnspan=4)
        #
        energy = tk.StringVar()
        aggression = tk.StringVar()
        tk.Label(root, text='Peak Energy:').grid(row=8, column=1, columnspan=2)
        tk.Label(root, text='Peak Aggression:').grid(row=8, column=3, columnspan=2)
        tk.Label(root, text="""
        1: Barely awake
        2: Calm
        3: Focused
        4: Mildly agitated
        5: Moderately agitated
        6: Very agitated
        7: Between 6 & 8
        8: Mild exertion
        9: Moderate exertion
        10: Heavy exertion
        """).grid(row=9, column=1)
        tk.Spinbox(root, bg='white', from_='1', to='10', increment='0.2', textvariable=energy).grid(row=9, column=2)
        tk.Label(root, text="""
        1: None
        2: Muttering
        3: Cursing
        4: Screaming and Cursing
        5: Rage Quitting
        6: Veiled Threatening
        7: Overt Threatening
        8: Minor Violence
        9: Moderate Violence
        10: Extreme Violence
        """).grid(row=9, column=3)
        tk.Spinbox(root, bg='white', from_='1', to='10', increment='0.2', textvariable=aggression).grid(row=9, column=4)
        #
        tk.Label(root, text='Outcome of the Event:').grid(row=10, column=1, columnspan=4)
        outcome = tk.Text(root, bg='white', width=t_width, height=4)
        outcome.grid(row=11, column=1, columnspan=4)
        #
        tk.Button(root, text='Confirm and Submit', pady=8, padx=8, command=partial(
            self.confirm,
            today,
            description,
            triggers,
            stressors,
            energy,
            aggression,
            outcome
        )).grid(row=12, column=2)
        tk.Button(root, text='Quit', pady=8, padx=8, command=root.destroy).grid(row=12, column=3)
        root.mainloop()
    

    def confirm(self, today, description, triggers, stressors, energy, aggression, outcome):
        description = description.get('1.0', 'end').rstrip('\n')
        triggers = triggers.get('1.0', 'end').rstrip('\n')
        stressors = stressors.get('1.0', 'end').rstrip('\n')
        energy = energy.get()
        aggression = aggression.get()
        outcome = outcome.get('1.0', 'end').rstrip('\n')
        for x in [today, description, triggers, stressors, energy, aggression, outcome]:
            print(x)
        #
        db = Connection('../me.db')
        curs = db.cursor()
        statement = 'INSERT INTO Burn_Log (Date, Description, Peak_Arousal, Peak_Aggression, Pre_Existing_Stressors, Trigger_Thoughts, Result) Values ("' + today + '", "' + description + '", ' + energy + ', ' + aggression + ', "' + stressors + '", "' + triggers + '", "' + outcome + '");'
        print(statement)
        curs.execute(statement)
        db.commit()


if __name__ == '__main__':
    Gui()