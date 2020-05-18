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


def parse(text, path='me.db'):
    #connect to our sql database:
    db = Connection(path)
    curs = db.cursor()
    # regular expressions for finding dates and days of the week:
    patt = re.compile(r'\d{1,2}\/\d{1,2}\/\d{1,2}')
    patt2 = re.compile(r'^([Ss]un|[Mm]on|[Tt]ues|[Ww]ednes|[Tt]hurs|[Ff]ri|[Ss]atur)day$')
    # start of our sql statement:
    stmt = "INSERT INTO Daily_Functionality (\
Weekday, Date, \
Project_Hours, Study_Hours, Administrative_Hours, Total_Work, \
Strength_Training, Cardio, Mobility, Total_Exercise, \
Social_Hours, Sleep_1, Sleep_2, Total_Sleep, \
Indulging, Flaking, Cursing, Intoxication, Total_Vices, \
Burnout, Quality_Of_Life\
) Values ("
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
            curs.execute(statement)
        except Exception as e:
            print(e)
            break
        # add 1 to count and repeat the loop for the next day:
        count += 1
    # commit transaction, close connection, return datetime.date() objects
    db.commit()
    curs.close(); db.close()
    return first_day, last_day


def compile_weekly(first_day, last_day, path='me.db'):
    # connect to the appropriate database:
    db = Connection(path)
    curs = db.cursor()
    # copy first_day to day and create the base sql statement to build on:
    day = first_day
    statement = 'INSERT INTO Weekly_Functionality (\
Starting_Date, Ending_Date, \
Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, \
Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, \
Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Sleep, \
Total_Indulging, Total_Flaking, Total_Cursing, Total_Intoxication, Total_Vices, \
Total_Burnout, Total_Quality_Of_Life\
) Values ("' + day.__str__() + '", "'
    #
    # get our OrderedDict and fill it with data:
    sums = ret_sums()
    for i in range(7):
        vals = curs.execute('SELECT * FROM Daily_Functionality WHERE Date="' + day.__str__() + '";').fetchall()
        sums['Total_Project_Hours'] += vals[0][2]
        sums['Total_Study_Hours'] += vals[0][3]
        sums['Total_Administrative_Hours'] += vals[0][4]
        sums['Total_Work'] += vals[0][5]
        sums['Total_Strength_Training'] += vals[0][6]
        sums['Total_Cardio'] += vals[0][7]
        sums['Total_Mobility'] += vals[0][8]
        sums['Total_Exercise'] += vals[0][9]
        sums['Total_Social_Hours'] += vals[0][10]
        sums['Total_Sleep_1'] += vals[0][11]
        sums['Total_Sleep_2'] += vals[0][12]
        sums['Total_Sleep'] += vals[0][13]
        sums['Total_Indulging'] += vals[0][14]
        sums['Total_Flaking'] += vals[0][15]
        sums['Total_Cursing'] += vals[0][16]
        sums['Total_Intoxication'] += vals[0][17]
        sums['Total_Vices'] += vals[0][18]
        sums['Total_Burnout'] += vals[0][19]
        sums['Total_Quality_Of_Life'] += vals[0][21]
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
        curs.execute(statement)
    except Exception as e:
        print(e)
    # commit the transaction and close the connection:
    db.commit()
    curs.close(); db.close()


def compile_monthly(month, year, path='me.db'):
    # connect to the appropriate sqlite database
    db = Connection(path)
    curs = db.cursor()
    # initialize the sql statement we will build on later:
    statement = 'INSERT INTO Monthly_Functionality (\
Starting_Date, Ending_Date, \
Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, \
Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, \
Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Sleep, \
Average_Indulging, Average_Flaking, Average_Cursing, Average_Intoxication, Average_Vices, \
Average_Burnout, Average_Quality_Of_Life\
) Values ("'
    # create and fill the sums OrderedDict
    sums = ret_sums()
    length = monthrange(year, month)[1] + 1
    for b in range(1, length):
        vals = curs.execute('SELECT * FROM Daily_Functionality WHERE Date="' + datetime.date(year, month, b).__str__() + '";').fetchall()
        sums['Total_Project_Hours'] += vals[0][2]
        sums['Total_Study_Hours'] += vals[0][3]
        sums['Total_Administrative_Hours'] += vals[0][4]
        sums['Total_Work'] += vals[0][5]
        sums['Total_Strength_Training'] += vals[0][6]
        sums['Total_Cardio'] += vals[0][7]
        sums['Total_Mobility'] += vals[0][8]
        sums['Total_Exercise'] += vals[0][9]
        sums['Total_Social_Hours'] += vals[0][10]
        sums['Total_Sleep_1'] += vals[0][11]
        sums['Total_Sleep_2'] += vals[0][12]
        sums['Total_Sleep'] += vals[0][13]
        sums['Total_Indulging'] += vals[0][14]
        sums['Total_Flaking'] += vals[0][15]
        sums['Total_Cursing'] += vals[0][16]
        sums['Total_Intoxication'] += vals[0][17]
        sums['Total_Vices'] += vals[0][18]
        sums['Total_Burnout'] += vals[0][19]
        sums['Total_Quality_Of_Life'] += vals[0][21]
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
            curs.execute(statement)
        except Exception as e:
            print(e)
            break
    # commit the transaction and close the database connections
    db.commit()
    curs.close(); db.close()


def compile_annual(first_day, last_day, path='me.db'):
    # connect to the database:
    db = Connection(path)
    curs = db.cursor()
    # Create the sql statement we will build on later:
    statement = 'INSERT INTO Annual_Functionality (\
Starting_Date, Ending_Date, \
Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, \
Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, \
Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Sleep, \
Total_Indulging, Total_Flaking, Total_Cursing, Total_Intoxication, Total_Vices, \
Total_Burnout, Total_Quality_Of_Life, \
Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, \
Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, \
Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Sleep, \
Average_Indulging, Average_Flaking, Average_Cursing, Average_Intoxication, Average_Vices, \
Average_Burnout, Average_Quality_Of_Life\
) Values ("' + first_day.__str__() + '", "' + last_day.__str__() + '", '
    # create and fill the sums OrderedDict
    sums = ret_sums()
    day = first_day
    length = (last_day - first_day).days + 1
    for a in range(length):
        vals = curs.execute('SELECT * FROM Daily_Functionality WHERE Date="' + day.__str__() + '";').fetchall()
        sums['Total_Project_Hours'] += vals[0][2]
        sums['Total_Study_Hours'] += vals[0][3]
        sums['Total_Administrative_Hours'] += vals[0][4]
        sums['Total_Work'] += vals[0][5]
        sums['Total_Strength_Training'] += vals[0][6]
        sums['Total_Cardio'] += vals[0][7]
        sums['Total_Mobility'] += vals[0][8]
        sums['Total_Exercise'] += vals[0][9]
        sums['Total_Social_Hours'] += vals[0][10]
        sums['Total_Sleep_1'] += vals[0][11]
        sums['Total_Sleep_2'] += vals[0][12]
        sums['Total_Sleep'] += vals[0][13]
        sums['Total_Indulging'] += vals[0][14]
        sums['Total_Flaking'] += vals[0][15]
        sums['Total_Cursing'] += vals[0][16]
        sums['Total_Intoxication'] += vals[0][17]
        sums['Total_Vices'] += vals[0][18]
        sums['Total_Burnout'] += vals[0][19]
        sums['Total_Quality_Of_Life'] += vals[0][21]
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
        curs.execute(statement)
    except Exception as e:
        print(e)
    # commit the transaction, close the database connection:
    db.commit()
    curs.close(); db.close()


def ret_sums():
    sums = OrderedDict()
    # these are the columns from the sqlite database
    # associated with values in the spreadsheet:
    sums['Total_Project_Hours'] = 0
    sums['Total_Study_Hours'] = 0
    sums['Total_Administrative_Hours'] = 0
    sums['Total_Work'] = 0
    sums['Total_Strength_Training'] = 0
    sums['Total_Cardio'] = 0
    sums['Total_Mobility'] = 0
    sums['Total_Exercise'] = 0
    sums['Total_Social_Hours'] = 0
    sums['Total_Sleep_1'] = 0
    sums['Total_Sleep_2'] = 0
    sums['Total_Sleep'] = 0
    sums['Total_Indulging'] = 0
    sums['Total_Flaking'] = 0
    sums['Total_Cursing'] = 0
    sums['Total_Intoxication'] = 0
    sums['Total_Vices'] = 0
    sums['Total_Burnout'] = 0
    sums['Total_Quality_Of_Life'] = 0
    #
    return sums


def main(lines, dry, path):
    # get values from tkinter objects:
    db = path.get()
    text = lines.get('1.0', 'end')
    dry_run = True if dry.get() == 1 else False
    # create a copy of me.db to work with if doing a dry run:
    if dry_run:
        dry_db = os.path.join(os.path.dirname(os.path.abspath(db)), 'dry.db')
        copy(db, dry_db)
        db = dry_db
    # print values for debugging:
    print('text:\n', text)
    print('dry_run:', dry_run)
    print('fileos.path.', db)
    print('\n\n')
    # process data for Daily_Functionality and Weekly_Functionality tables:
    first_day, last_day = parse(text, db)
    compile_weekly(first_day, last_day, db)
    # process data for Monthly_Functionality if we just ended the month:
    if last_day.day < 7 or last_day == monthrange(first_day.year, first_day.month)[1]:
        month = first_day.month
        year = first_day.year
        compile_monthly(month, year, db)
    # process data for Annual_Functionality if we just ended the year:
    if (last_day.month == 1 and last_day.day < 7) or (last_day.month == 12 and last_day.day == 31):
        d1 = datetime.date(first_day.year, 1, 1)
        d2 = datetime.date(first_day.year, 12, 31)
        compile_annual(d1, d2, db)
    # prompt user before deleting dry.db, if applicable:
    if dry_run:
        input('Type any key when it is okay to remove the temporary database, dry.db:\n')
        os.remove(db)


class Gui:
    def __init__(self):
        root = tk.Tk()
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
        # where is me.db?
        path = tk.StringVar()
        filepath = tk.Entry(root, width=80, bg='white', textvariable=path)
        filepath.grid(row=3, column=1)
        tk.Button(root, text='Find me.db', command=(
            lambda x=filepath:[x.delete(0, len(x.get())), x.insert(0, askopenfilename())]
        )).grid(row=3, column=2)
        # buttons to start or quit:
        process = tk.Button(root, text='Process Text', command=partial(
            main, lines, dry_run, path
        ))
        process.grid(row=4, column=1)
        tk.Button(root, text='Quit', command=root.destroy).grid(row=4, column=2)
        # keybinding and gui initialization:
        root.bind(sequence='<Return>', func=partial(main, lines, dry_run, path))
        root.mainloop()


if __name__ == '__main__':
    # initialize the gui:
    Gui()