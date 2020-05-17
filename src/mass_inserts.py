import re, sqlite3, datetime, calendar
from collections import OrderedDict

"""
# These are the crude and dirty functions I used 
# to build the sqlite database in the first place
# using python3:
import os
os.chdir(<path_to_me.db_directory>)
import src.mass_inserts
# for each week:
text='''<copy+paste a week's worth of spreadsheet data>'''
mass_inserts.parse(text)
# then:
import datetime
d1 = datetime.date(year, month, day) # of first Sunday in dataset
d2 = datetime.date(year, month, day) # of last Sunday in dataset
mass_inserts.compile_weekly(d1, d2)
mass_inserts.compile_monthly()
# for each year in dataset:
d1 = datetime.date(year, 1, 1)
d2 = datetime.date(year, 12, 31)
mass_inserts.compile_annual(d1, d2)
"""


def parse(text):
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    patt = re.compile(r'^\d{1,2}\/\d{1,2}\/\d{1,2}')
    patt2 = re.compile(r'^([Ss]un|[Mm]on|[Tt]ues|[Ww]ednes|[Tt]hurs|[Ff]ri|[Ss]atur)day$')
    #
    statement1 = "INSERT INTO Daily_Functionality (\
Weekday, Date, \
Project_Hours, Study_Hours, Administrative_Hours, Total_Work, \
Strength_Training, Cardio, Mobility, Total_Exercise, \
Social_Hours, Sleep_1, Sleep_2, Total_Sleep, \
Burnout, Quality_Of_Life\
) Values ("
    statement2 = "INSERT INTO Daily_Functionality (\
Weekday, Date, \
Project_Hours, Study_Hours, Administrative_Hours, Total_Work, \
Strength_Training, Cardio, Mobility, Total_Exercise, \
Social_Hours, Sleep_1, Sleep_2, Total_Sleep, \
Indulging, Flaking, Cursing, Intoxication, Total_Vices, \
Burnout, Quality_Of_Life\
) Values ("
    #
    count = 0
    for x in text.split('\n'):
        if count >= 7:
            break
        #
        a = x.split('\t')
        b = a[1].strip(' ')
        vals = b.split('/')
        vals[2] = '20' + vals[2]
        vals = [int(c.lstrip('0')) for c in vals]
        if datetime.date(vals[2], vals[0], vals[1]) < datetime.date(2019, 9, 29):
            statement = statement1
        else:
            statement = statement2
        #i
        for y in x.split('\t'):
            y = y.strip(' ')
            if re.match(patt, y):
                vals = y.split('/')
                vals[2] = '20' + vals[2]
                vals = [vals[2], vals[0], vals[1]]
                z = '-'.join(vals)
                statement += '"' + z + '", '
                continue
            elif re.match(patt2, y):
                statement += '"' + y + '", '
                continue
            statement += y + ', '
        statement = re.sub(r', $', r'', statement)
        statement += ');'
        #
        print(statement)
        print('\n\n')
        try:
            curs.execute(statement)
        except Exception as e:
            print(e)
            break
        #
        count += 1
    #
    db.commit()
    curs.close(); db.close()


def compile_weekly(first_day, last_day):
    # first_day must be a datetime.date() object representing the first 
    # Sunday of the week to be compiled and inserted.
    # last_day must be a datetime.date() object representing
    # the last Sunday of a full week in the Daily_Functionality table.
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    day = first_day
    shift_date = datetime.date(2019, 9, 29)
    while day <= last_day:
        if day <= shift_date:
            sums = OrderedDict()
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
            sums['Total_Burnout'] = 0
            sums['Total_Quality_Of_Life'] = 0
            statement = 'INSERT INTO Weekly_Functionality (\
Starting_Date, Ending_Date, \
Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, \
Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, \
Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Sleep, \
Total_Burnout, Total_Quality_Of_Life\
) Values ("' + day.__str__() + '", "'
            #
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
                sums['Total_Burnout'] += vals[0][19]
                sums['Total_Quality_Of_Life'] += vals[0][21]
                #
                day += datetime.timedelta(days=1)
                if i == 5:
                    statement += day.__str__() + '", '
            #
            for x in sums.keys():
                statement += str(sums[x]) + ', '
            statement = re.sub(r', $', r'', statement)
            statement += ');'
            print(statement)
            print('\n\n')
            try:
                curs.execute(statement)
            except Exception as e:
                print(e)
                break
        #
        else:
            sums = OrderedDict()
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
            statement = 'INSERT INTO Weekly_Functionality (\
Starting_Date, Ending_Date, \
Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, \
Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, \
Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Sleep, \
Total_Indulging, Total_Flaking, Total_Cursing, Total_Intoxication, Total_Vices, \
Total_Burnout, Total_Quality_Of_Life\
) Values ("' + day.__str__() + '", "'
            #
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
                #
                day += datetime.timedelta(days=1)
                if i == 5:
                    statement += day.__str__() + '", '
            #
            for x in sums.keys():
                statement += str(sums[x]) + ', '
            statement = re.sub(r', $', r'', statement)
            statement += ');'
            print(statement)
            print('\n\n')
            try:
                curs.execute(statement)
            except Exception as e:
                print(e)
                break
    #
    db.commit()
    curs.close(); db.close()


def compile_monthly():
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    statement1 = 'INSERT INTO Monthly_Functionality (\
Starting_Date, Ending_Date, \
Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, \
Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, \
Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Sleep, \
Average_Burnout, Average_Quality_Of_Life\
) Values ("'
    statement2 = 'INSERT INTO Monthly_Functionality (\
Starting_Date, Ending_Date, \
Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, \
Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, \
Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Sleep, \
Average_Indulging, Average_Flaking, Average_Cursing, Average_Intoxication, Average_Vices, \
Average_Burnout, Average_Quality_Of_Life\
) Values ("'
    #
    sums = OrderedDict()
    # 2019
    for a in range(4, 13):
        sums = OrderedDict()
        if a < 10:
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
            sums['Total_Burnout'] = 0
            sums['Total_Quality_Of_Life'] = 0
        else:
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
        length = calendar.monthrange(2019, a)[1] + 1
        for b in range(1, length):
            vals = curs.execute('SELECT * FROM Daily_Functionality WHERE Date="' + datetime.date(2019, a, b).__str__() + '";').fetchall()
            if a < 10:
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
                sums['Total_Burnout'] += vals[0][19]
                sums['Total_Quality_Of_Life'] += vals[0][21]
            else:
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
        # prepare the statement next at this level:
        if a < 10:
            statement = statement1
        else:
            statement = statement2
        averages = OrderedDict()
        for c in sums.keys():
            key = c.replace('Total', 'Average')
            averages[key] = sums[c] / length
        statement += datetime.date(2019, a, 1).__str__() + '", "'
        statement += datetime.date(2019, a, length-1).__str__() + '", '
        for d in averages.keys():
            statement += str(averages[d]) + ', '
        statement = re.sub(r', $', r'', statement)
        statement += ');'
        #
        print(statement)
        print('\n\n')
        try:
            curs.execute(statement)
        except Exception as e:
            print(e)
            break
    # 2020
    for a in range(1, 5):
        sums = OrderedDict()
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
        length = calendar.monthrange(2020, a)[1] + 1
        for b in range(1, length):
            vals = curs.execute('SELECT * FROM Daily_Functionality WHERE Date="' + datetime.date(2020, a, b).__str__() + '";').fetchall()
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
        # prepare the statement:
        statement = statement2
        averages = OrderedDict()
        for c in sums.keys():
            key = c.replace('Total', 'Average')
            averages[key] = sums[c] / length
        statement += datetime.date(2020, a, 1).__str__() + '", "'
        statement += datetime.date(2020, a, length-1).__str__() + '", '
        for d in averages.keys():
            statement += str(averages[d]) + ', '
        statement = re.sub(r', $', r'', statement)
        statement += ');'
        #
        print(statement)
        print('\n\n')
        try:
            curs.execute(statement)
        except Exception as e:
            print(e)
            break

    db.commit()
    curs.close(); db.close()


def compile_annual(first_day, last_day):
    # first_day and last_day must be datetime.date objects representing
    # the first and last day of data represented in the database for the year
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    shift_date = datetime.date(2019, 9, 29)
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
    #
    sums = OrderedDict()
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
        sums['Total_Burnout'] += vals[0][19]
        sums['Total_Quality_Of_Life'] += vals[0][21]
        if day > shift_date:
            sums['Total_Indulging'] += vals[0][14]
            sums['Total_Flaking'] += vals[0][15]
            sums['Total_Cursing'] += vals[0][16]
            sums['Total_Intoxication'] += vals[0][17]
            sums['Total_Vices'] += vals[0][18]
        #
        day += datetime.timedelta(days=1)
    #
    try:
        assert day == (last_day + datetime.timedelta(days=1))
    except AssertionError:
        print('length:', length)
        print('day:', day)
        print('last_day:', last_day)
        return
    averages = OrderedDict()
    for c in sums.keys():
        statement += str(sums[c]) + ', '
        key = c.replace('Total', 'Average')
        if c in ['Total_Indulging', 'Total_Flaking', 'Total_Cursing', 'Total_Intoxication', 'Total_Vices'] and last_day.year == 2019:
            averages[key] = sums[c] / ((last_day - shift_date).days + 1)
        else:
            averages[key] = sums[c] / length
    for d in averages.keys():
        statement += str(averages[d]) + ', '
    statement = re.sub(r', $', r'', statement)
    statement += ');'
    print(statement)
    try:
        curs.execute(statement)
    except Exception as e:
        print(e)
    #
    db.commit()
    curs.close(); db.close()