import re, sqlite3
import datetime


patt = re.compile(r'^\d{1,2}\/\d{1,2}\/\d{1,2}')
patt2 = re.compile(r'^([Ss]un|[Mm]on|[Tt]ues|[Ww]ednes|[Tt]hurs|[Ff]ri|[Ss]atur)day$')


def parse(text):
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    statement1 = "INSERT INTO Daily_Functionality (Weekday, Date, Project_Hours, Study_Hours, Administrative_Hours, Total_Work, Strength_Training, Cardio, Mobility, Total_Exercise, Social_Hours, Sleep_1, Sleep_2, Total_Replenishing, Burnout, Quality_Of_Life) Values ("
    statement2 = "INSERT INTO Daily_Functionality (Weekday, Date, Project_Hours, Study_Hours, Administrative_Hours, Total_Work, Strength_Training, Cardio, Mobility, Total_Exercise, Social_Hours, Sleep_1, Sleep_2, Total_Replenishing, Indulging, Flaking, Cursing, Intoxication, Total_Vices, Burnout, Quality_Of_Life) Values ("
    #
    count = 0
    for x in text.split('\n'):
        if count >= 7:
            break
        for y in x.split('\t'):
            y = y.strip(' ')
            if re.match(patt, y):
                vals = y.split('/')
                vals[2] = '20' + vals[2]
                vals = [int(z.lstrip('0')) for z in vals]
                if datetime.date(vals[2], vals[0], vals[1]) < datetime.date(2019, 9, 29):
                    statement = statement1
                else:
                    statement = statement2
                break
        for y in x.split('\t'):
            y = y.strip(' ')
            if re.match(patt, y):
                vals = y.split('/')
                vals[2] = '20' + vals[2]
                vals = [int(z.lstrip('0')) for z in vals]
                vals = [vals[2], vals[0], vals[1]]
                z = '-'.join([str(a) for a in vals])
                statement += '"' + z + '", '
                continue
            elif re.match(patt2, y):
                statement += '"' + y + '", '
                continue
            statement += y + ', '
        statement = re.sub(r', $', r'', statement)
        statement += ');'
        #
        #print(statement, end='\n\n\n')
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


def compile_weekly():
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    statement1 = "INSERT INTO Weekly_Functionality (Starting_Date, Ending_Date, Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Replenishing, Total_Burnout, Total_Over_Extending, Total_Quality_Of_Life) Values ("
    statement2 = "INSERT INTO Weekly_Functionality (Starting_Date, Ending_Date, Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Replenishing, Total_Indulging, Total_Flaking, Total_Cursing, Total_Intoxication, Total_Vices, Total_Burnout, Total_Over_Extending, Total_Quality_Of_Life) Values ("
    #
    # lots of stuff
    #
    db.commit()


def compile_monthly():
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    statement = "INSERT INTO Monthly_Functionality (Starting_Date, Ending_Date, Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Replenishing, Average_Indulging, Average_Flaking, Average_Cursing, Average_Intoxication, Average_Vices, Average_Burnout, Average_Over_Extending, Average_Quality_Of_Life) Values ("
    #
    # lots of stuff
    #
    db.commit()


def compile_annual():
    db = sqlite3.Connection('me.db')
    curs = db.cursor()
    #
    statement = ""
    #
    # lots of stuff
    #
    db.commit()