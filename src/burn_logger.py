#!/usr/bin/env python3

"""
Documentation and such...
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from datetime import date
from functools import partial
from sqlite3 import Connection
from os import getcwd


class Gui:
    def __init__(self):
        root = tk.Tk()
        root.title('Burn Log')
        # Labels and text entries for describing the event:
        today = date.today().__str__()
        tk.Label(root, text='Burn Log').grid(row=1, column=1, columnspan=2)
        tk.Label(root, text='Date: ' + today).grid(row=1, column=3, columnspan=2)
        tk.Label(root, text='Description of Event:').grid(row=2, column=1, columnspan=4)
        description = tk.Text(root, bg='white', width=80, height=3)
        description.grid(row=3, column=1, columnspan=4)
        tk.Label(root, text='Trigger Thoughts ("Shoulds" and Blamers, separated by "|"):').grid(row=4, column=1, columnspan=4)
        triggers = tk.Text(root, bg='white', width=80, height=3)
        triggers.grid(row=5, column=1, columnspan=4)
        # spinboxes describing the severity of the incident:
        energy = tk.StringVar()
        aggression = tk.StringVar()
        tk.Label(root, text='Peak Energy:').grid(row=9, column=1, columnspan=2)
        tk.Label(root, text='Peak Aggression:').grid(row=9, column=3, columnspan=2)
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
        """).grid(row=10, column=1)
        tk.Spinbox(root, bg='white', from_='1', to='10', increment='0.2', width=4, textvariable=energy).grid(row=10, column=2)
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
        """).grid(row=10, column=3)
        tk.Spinbox(root, bg='white', from_='1', to='10', increment='0.2', width=4, textvariable=aggression).grid(row=10, column=4)
        # Text widget to describe the outcome in:
        tk.Label(root, text='Outcome of the Event:').grid(row=11, column=1, columnspan=4)
        outcome = tk.Text(root, bg='white', width=80, height=3)
        outcome.grid(row=12, column=1, columnspan=4)
        # Frame for checkboxes to mark all the common triggers that were present:
        frm = tk.Frame(root)
        # get all columns from Burn_Factors table indicating common triggers,
        # put them into list called cols
        db = Connection('me.db')
        curs = db.cursor()
        cols = curs.execute('pragma table_info(Burn_Factors)').fetchall()
        curs.close(); db.close()
        # label the Frame
        tk.Label(frm, text='Factors:').grid(row=1, column=1, columnspan=8)
        # create burn_factor dictionary
        burn_factors = {}
        # loop through cols, creating rows of up to 4 labels and 4 checkboxes,
        rownum = 2; colnum = 1
        for x in cols:
            # make sure it is one of the boolean values
            if x[2] == 'INTEGER' and x[1] not in ['Total_Factors', 'Other']:
                # label each checkbox, with each IntVar corresponding to an entry in the burn_factors dictionary
                var = tk.IntVar()
                tk.Label(frm, text=x[1]).grid(row=rownum, column=colnum)
                colnum += 1
                tk.Checkbutton(frm, offvalue=0, onvalue=1, variable=var).grid(row=rownum, column=colnum)
                colnum += 1
                # move to a new row if we have filled 8 columns:
                if colnum % 9 == 0:
                    colnum = 1
                    rownum += 1
                # add the IntVar to the dictionary
                burn_factors[x[1]] = var
        rownum += 1
        # Text box for describing uncommon triggers:
        tk.Label(frm, text='Other Factors:').grid(row=rownum, column=1, columnspan=8)
        other_factors = tk.Text(frm, bg='white', width=80, height=3)
        other_factors.grid(row=rownum+1, column=1, columnspan=8)
        burn_factors['Other'] = other_factors
        frm.grid(row=13, column=1, columnspan=4)
        # help python locate the correct database:
        tk.Label(root, text='Find me.db :').grid(row=14, column=1)
        filepath = tk.StringVar()
        entry = tk.Entry(root, bg='white', textvariable=filepath, width=50)
        entry.grid(row=14, column=2, columnspan=2)
        tk.Button(root, text='Browse', command=(
            lambda x=entry:[x.delete(0, len(x.get())), x.insert(0, askopenfilename())]
        )).grid(row=14, column=4)
        # Buttons to create and execute the sql statement or quit the application
        tk.Button(root, text='Confirm and Submit', pady=8, padx=8, command=partial(
            self.confirm,
            today,
            description,
            triggers,
            energy,
            aggression,
            outcome,
            burn_factors,
            filepath
        )).grid(row=15, column=2)
        tk.Button(root, text='Quit', pady=8, padx=8, command=root.destroy).grid(row=15, column=3)
        # keybinding and gui initialization:
        root.bind(sequence='<Return>', func=partial(
            self.confirm,
            today,
            description,
            triggers,
            energy,
            aggression,
            outcome,
            burn_factors,
            filepath
        ))
        root.mainloop()
    

    def confirm(self, today, description, triggers, energy, aggression, outcome, burn_factors, filepath):
        # get intelligible values from tkinter variables
        description = description.get('1.0', 'end').rstrip('\n')
        triggers = triggers.get('1.0', 'end').rstrip('\n')
        energy = energy.get()
        aggression = aggression.get()
        outcome = outcome.get('1.0', 'end').rstrip('\n')
        # create the sql statement for the Burn_Log table
        log_statement = 'INSERT INTO Burn_Log (Date, Description, Peak_Arousal, Peak_Aggression, Trigger_Thoughts, Result) Values ("' + today + '", "' + description + '", ' + energy + ', ' + aggression + ', "' + triggers + '", "' + outcome + '");'
        print(log_statement)
        # begin 2 parts for sql statement for Burn_Factors table:
        factors = 0
        factors_statement = 'INSERT INTO Burn_Factors (Date, '
        values = 'Values ("' + today + '", '
        # loop through burn_factors dictionary, 
        # adding to the separate parts of thesql statement
        # where non-zero values are found:
        for x in burn_factors.keys():
            print(x, burn_factors[x])
            if x == 'Other':
                other_factor = burn_factors[x].get('1.0', 'end')
                other_factor = other_factor.rstrip('\n')
                if other_factor != '':
                    factors_statement += 'Other, '
                    values += '"' + other_factor + '", '
                    factors += 1
            elif burn_factors[x].get() == 1:
                factors_statement += x + ', '
                values += '1, '
                factors += 1
        # finish the two parts of the statement and combine them:
        factors_statement += 'Total_Factors) '
        values += str(factors) + ');'
        factors_statement += values
        print(factors_statement)
        # show the sql to the user and ask for confirmation before running it:
        sprout = tk.Toplevel()
        tk.Label(sprout, text='Confirm:').pack()
        tk.Label(sprout).pack()
        tk.Label(sprout, text=log_statement, wraplength=800, justify='left').pack()
        tk.Label(sprout).pack()
        tk.Label(sprout, text=factors_statement, wraplength=800, justify='left').pack()
        tk.Label(sprout).pack()
        tk.Button(sprout, text='Confirm', command=partial(self.commit, sprout, log_statement, factors_statement, filepath)).pack()
        tk.Button(sprout, text='Cancel', command=sprout.destroy).pack()
        

    def commit(self, sprout, log_statement, factors_statement, filepath):
        # connect to the sql database, execute the statement
        # commit the transaction and close the connection:
        db = Connection(filepath.get())
        curs = db.cursor()
        curs.execute(log_statement)
        curs.execute(factors_statement)
        db.commit()
        curs.close(); db.close()
        sprout.destroy()


if __name__ == '__main__':
    Gui()