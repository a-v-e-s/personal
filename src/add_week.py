#!/usr/bin/env python3

"""
Documentation and such....
"""

import re, datetime, os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from sqlite3 import Connection
from calendar import monthrange
from shutil import copy
from functools import partial
from collections import OrderedDict
from time import sleep
import statements, get_cursor


def parse(text, cursor):
    #connect to our sql database:
    #db = Connection(path)
    #curs = db.cursor()
    # regular expressions for finding dates and days of the week:
    patt = re.compile(r'\d{1,2}\/\d{1,2}\/\d{1,2}')
    patt2 = re.compile(r'^([Ss]un|[Mm]on|[Tt]ues|[Ww]ednes|[Tt]hurs|[Ff]ri|[Ss]atur)day$')
    # start of our sql statement:
    stmt = statements.insert_daily
    # one iteration for each day of the week's data:
    count = 0
    for x in text.split('\n'):
        # renew the statement
        # do special things with Sunday and Saturday's data:
        statement = stmt
        if count == 0: # Sunday
            first = re.search(patt, x).group(0).split('/')
            first_day = datetime.date(int('20'+first[2]), int(first[0]), int(first[1]))
        elif count == 6: # Saturday
            last = re.search(patt, x).group(0).split('/')
            last_day = datetime.date(int('20'+last[2]), int(last[0]), int(last[1]))
        elif count >= 7:
            break
        # for each item in the line, add it to the statement:
        for y in x.split('\t'):
            y = y.strip(' ')
            if re.match(patt2, y): # this is the first item
                statement += '"' + y + '", '
                continue
            if re.match(patt, y): # this is the second item
                # create list called vals 
                # with integers for year, month, day,
                # add these vales to the statement:
                vals = y.split('/')
                vals[2] = '20' + vals[2]
                vals = [vals[2], vals[0], vals[1]]
                z = '-'.join(vals)
                statement += '"' + z + '", '
                continue
            # otherwise add the numeric value a comma and space:
            statement += y + ', '
        # close the statement out:
        statement = re.sub(r', $', r'', statement)
        statement += ');'
        # print and execute the statement we have crafted
        print(statement)
        print('\n\n')
        try:
            cursor.execute(statement)
        except Exception as e:
            print(e)
            break
        # add 1 to count and repeat the loop for the next day:
        count += 1
    # commit transaction, close connection, return datetime.date() objects
    #db.commit()
    #curs.close(); db.close()
    return first_day, last_day


def compile_weekly(first_day, last_day, cursor):
    # connect to the appropriate database:
    #db = Connection(path)
    #curs = db.cursor()
    # copy first_day to day and create the base sql statement to build on:
    day = first_day
    statement = statements.insert_weekly + day.__str__() + '", "'
    #
    # get our OrderedDict and fill it with data:
    sums = statements.ret_sums()
    for i in range(7):
        vals = cursor.execute('SELECT * FROM Daily_Functionality WHERE Date="' + day.__str__() + '";').fetchall()
        #
        sums = tally_sums(sums, vals)
        # move to the next day
        day += datetime.timedelta(days=1)
        if i == 5: # We are on Saturday, the Ending_Date for the week:
            statement += day.__str__() + '", '
    # add data from the OrderedDict to the statement:
    for x in sums.keys():
        statement += str(sums[x]) + ', '
    statement = re.sub(r', $', r'', statement)
    statement += ');'
    # print and execute the statement:
    print(statement)
    print('\n\n')
    try:
        cursor.execute(statement)
    except Exception as e:
        print(e)
    # commit the transaction and close the connection:
    #db.commit()
    #curs.close(); db.close()


def compile_monthly(month, year, cursor):
    # connect to the appropriate sqlite database
    #db = Connection(path)
    #curs = db.cursor()
    # initialize the sql statement we will build on later:
    statement = statements.insert_monthly
    # create and fill the sums OrderedDict
    sums = statements.ret_sums()
    length = monthrange(year, month)[1] + 1
    for b in range(1, length):
        vals = cursor.execute(
            'SELECT * FROM Daily_Functionality WHERE Date="' +
            datetime.date(year, month, b).__str__() +
            '";'
        ).fetchall()
        sums = tally_sums(sums, vals)
        # create the averages dict from sums
    averages = OrderedDict()
    for c in sums.keys():
        key = c.replace('Total', 'Average')
        averages[key] = sums[c] / length
    # complete the sql statement:
    statement += datetime.date(2020, month, 1).__str__() + '", "'
    statement += datetime.date(2020, month, length-1).__str__() + '", '
    for d in averages.keys():
        statement += str(averages[d]) + ', '
    statement = re.sub(r', $', r'', statement)
    statement += ');'
    # print and execute the statement
    print(statement)
    print('\n\n')
    try:
        cursor.execute(statement)
    except Exception as e:
        print(e)
    # commit the transaction and close the database connections
    #db.commit()
    #curs.close(); db.close()


def compile_annual(first_day, last_day, cursor):
    # connect to the database:
    #db = Connection(path)
    #curs = db.cursor()
    # Create the sql statement we will build on later:
    statement = statements.insert_annually + first_day.__str__() + '", "' + last_day.__str__() + '", '
    # create and fill the sums OrderedDict
    sums = statements.ret_sums()
    day = first_day
    length = (last_day - first_day).days + 1
    for a in range(length):
        vals = cursor.execute('SELECT * FROM Daily_Functionality WHERE Date="' + day.__str__() + '";').fetchall()
        sums = tally_sums(sums, vals)
        day += datetime.timedelta(days=1)
    # make sure we are on the right day:
    try:
        assert day == (last_day + datetime.timedelta(days=1))
    except AssertionError:
        # debugging information
        print('length:', length)
        print('day:', day)
        print('last_day:', last_day)
        return
    # create and fill the averages OrderedDict,
    # while also filling out the statement:
    averages = OrderedDict()
    for c in sums.keys():
        statement += str(sums[c]) + ', '
        key = c.replace('Total', 'Average')
        averages[key] = sums[c] / length
    for d in averages.keys():
        statement += str(averages[d]) + ', '
    statement = re.sub(r', $', r'', statement)
    statement += ');'
    # print and execute the statement:
    print(statement)
    print('\n\n')
    try:
        cursor.execute(statement)
    except Exception as e:
        print(e)
    # commit the transaction, close the database connection:
    #db.commit()
    #curs.close(); db.close()


def tally_sums(sums, vals):
    # loop through each sql column number in vals,
    # adding value to corresponding dictionary entry in sums:
    k = 0
    for i in range(1, 22):
    	if i not in [1, 20]: # [1, 20] aren't used
    		sums[statements.keys[k]] += vals[0][i]
    		k += 1
    # 
    return sums



def main(lines, dry, path):
    # get values from tkinter objects:
    path = path.get()
    text = lines.get('1.0', 'end')
    dry_run = True if dry.get() == 1 else False
    # create a copy of me.db to work with if doing a dry run:
    if dry_run:
        cur_db = os.path.abspath(path)
        dry_db = os.path.join(os.path.dirname(os.path.abspath(path)), 'dry.db')
        copy(cur_db, dry_db)
        cursor, db = get_cursor.get_cursor(dry_db, get_db=True)
    else:
        cursor, db = get_cursor.get_cursor(path, get_db=True)
    # print values for debugging:
    print('text:\n', text)
    print('dry_run:', dry_run)
    print('fileos.path.', db)
    print('\n\n')
    # process data for Daily_Functionality and Weekly_Functionality tables:
    first_day, last_day = parse(text, cursor)
    compile_weekly(first_day, last_day, cursor)
    # process data for Monthly_Functionality if we just ended the month:
    if last_day.day < 7 or last_day == monthrange(first_day.year, first_day.month)[1]:
        month = first_day.month
        year = first_day.year
        compile_monthly(month, year, cursor)
    # process data for Annual_Functionality if we just ended the year:
    if (last_day.month == 1 and last_day.day < 7) or (last_day.month == 12 and last_day.day == 31):
        d1 = datetime.date(first_day.year, 1, 1)
        d2 = datetime.date(first_day.year, 12, 31)
        compile_annual(d1, d2, cursor)
    # prompt user before deleting dry.db, if applicable:
    if dry_run:
        input('Type any key when it is okay to remove the temporary database, dry.db:\n')
        os.remove(dry_db)
    # close the cursor and the database connection:
    db.commit()
    cursor.close(); db.close()


class Gui:
    def __init__(self, path='me.db'):
        root = tk.Tk() if __name__ == '__main__' else tk.Toplevel()
        # copy and past text here:
        tk.Label(root, text="Copy + Paste a Week's Worth of Lines Here:").grid(row=0, column=0, columnspan=2)
        lines = tk.Text(root, bg='white', width=80, height=24)
        lines.grid(row=1, column=1, columnspan=2)
        # are we doing a dry run?
        tk.Label(root, text='Dry run?\n(Checked ==> dry_run=True)').grid(row=2, column=1)
        dry_run = tk.IntVar()
        dry = tk.Checkbutton(root, variable=dry_run, offvalue=0, onvalue=1)
        dry.grid(row=2, column=2)
        dry.select()
        # tkinter widgets to find 'me.db':
        tk.Label(root, text='Type path of "me.db":').grid(row=3, column=1, columnspan=2)
        path = tk.Entry(root, width=80)
        path.grid(row=4, column=1)
        finder = tk.Button(root, text='Browse', command=(
            lambda x=path: x.insert(0, askopenfilename())
        ))
        finder.grid(row=4, column=2)
        # buttons to start or quit:
        process = tk.Button(root, text='Process Text', command=partial(
            main, lines, dry_run, path
        ))
        process.grid(row=5, column=1)
        tk.Button(root, text='Quit', command=root.destroy).grid(row=5, column=2)
        # keybinding and gui initialization:
        root.bind(sequence='<Return>', func=partial(main, lines, dry_run, path))
        root.mainloop()


if __name__ == '__main__':
    # make sure we are in the correct directory:
    try:
        assert 'me.db' in os.listdir()
    except AssertionError as e:
        print(e)
        print('Not in same directory as "me.db"')
        exit(1)
    # if that checks out, initialize the gui:
    Gui('me.db')