"""
Details not to be made public.
Mostly a common location for lengthy sql statements.
"""

from collections import OrderedDict


create_daily = "CREATE TABLE Daily_Functionality ( \
Date TEXT PRIMARY KEY NOT NULL, \
Weekday TEXT NOT NULL, \
Project_Hours REAL NOT NULL DEFAULT 0, \
Study_Hours REAL NOT NULL DEFAULT 0, \
Administrative_Hours REAL NOT NULL DEFAULT 0, \
Total_Work REAL NOT NULL DEFAULT 0, \
Strength_Training REAL NOT NULL DEFAULT 0, \
Cardio REAL NOT NULL DEFAULT 0, \
Mobility REAL NOT NULL DEFAULT 0, \
Total_Exercise REAL NOT NULL DEFAULT 0, \
Social_Hours REAL NOT NULL DEFAULT 0, \
Sleep_1 REAL NOT NULL DEFAULT 0, \
Sleep_2 REAL NOT NULL DEFAULT 0, \
Total_Sleep REAL NOT NULL DEFAULT 0, \
Indulging REAL NOT NULL DEFAULT 0, \
Flaking REAL NOT NULL DEFAULT 0, \
Cursing REAL NOT NULL DEFAULT 0, \
Intoxication REAL NOT NULL DEFAULT 0, \
Total_Vices REAL NOT NULL DEFAULT 0, \
Burnout REAL NOT NULL DEFAULT 0, \
Over_Extending REAL NOT NULL DEFAULT 0, \
Quality_Of_Life REAL NOT NULL DEFAULT 0, \
Notes TEXT \
);"

create_weekly = "CREATE TABLE Weekly_Functionality ( \
Starting_Date TEXT PRIMARY KEY NOT NULL, \
Ending_Date TEXT NOT NULL, \
Total_Project_Hours REAL NOT NULL DEFAULT 0, \
Total_Study_Hours REAL NOT NULL DEFAULT 0, \
Total_Administrative_Hours REAL NOT NULL DEFAULT 0, \
Total_Work REAL NOT NULL DEFAULT 0, \
Total_Strength_Training REAL NOT NULL DEFAULT 0, \
Total_Cardio REAL NOT NULL DEFAULT 0, \
Total_Mobility REAL NOT NULL DEFAULT 0, \
Total_Exercise REAL NOT NULL DEFAULT 0, \
Total_Social_Hours REAL NOT NULL DEFAULT 0, \
Total_Sleep_1 REAL NOT NULL DEFAULT 0, \
Total_Sleep_2 REAL NOT NULL DEFAULT 0, \
Total_Sleep REAL NOT NULL DEFAULT 0, \
Total_Indulging REAL NOT NULL DEFAULT 0, \
Total_Flaking REAL NOT NULL DEFAULT 0, \
Total_Cursing REAL NOT NULL DEFAULT 0, \
Total_Intoxication REAL NOT NULL DEFAULT 0, \
Total_Vices REAL NOT NULL DEFAULT 0, \
Total_Burnout REAL NOT NULL DEFAULT 0, \
Total_Over_Extending REAL NOT NULL DEFAULT 0, \
Total_Quality_Of_Life REAL NOT NULL DEFAULT 0 \
);"

create_monthly = "CREATE TABLE Monthly_Functionality ( \
Starting_Date TEXT PRIMARY KEY NOT NULL, \
Ending_Date TEXT NOT NULL, \
Average_Project_Hours REAL NOT NULL DEFAULT 0, \
Average_Study_Hours REAL NOT NULL DEFAULT 0, \
Average_Administrative_Hours REAL NOT NULL DEFAULT 0, \
Average_Work REAL NOT NULL DEFAULT 0, \
Average_Strength_Training REAL NOT NULL DEFAULT 0, \
Average_Cardio REAL NOT NULL DEFAULT 0, \
Average_Mobility REAL NOT NULL DEFAULT 0, \
Average_Exercise REAL NOT NULL DEFAULT 0, \
Average_Social_Hours REAL NOT NULL DEFAULT 0, \
Average_Sleep_1 REAL NOT NULL DEFAULT 0, \
Average_Sleep_2 REAL NOT NULL DEFAULT 0, \
Average_Sleep REAL NOT NULL DEFAULT 0, \
Average_Indulging REAL NOT NULL DEFAULT 0, \
Average_Flaking REAL NOT NULL DEFAULT 0, \
Average_Cursing REAL NOT NULL DEFAULT 0, \
Average_Intoxication REAL NOT NULL DEFAULT 0, \
Average_Vices REAL NOT NULL DEFAULT 0, \
Average_Burnout REAL NOT NULL DEFAULT 0, \
Average_Over_Extending REAL NOT NULL DEFAULT 0, \
Average_Quality_Of_Life REAL NOT NULL DEFAULT 0 \
);"

create_annually = "CREATE TABLE Annual_Functionality ( \
Starting_Date TEXT PRIMARY KEY NOT NULL, \
Ending_Date TEXT NOT NULL, \
Total_Project_Hours REAL NOT NULL DEFAULT 0, \
Total_Study_Hours REAL NOT NULL DEFAULT 0, \
Total_Administrative_Hours REAL NOT NULL DEFAULT 0, \
Total_Work REAL NOT NULL DEFAULT 0, \
Total_Strength_Training REAL NOT NULL DEFAULT 0, \
Total_Cardio REAL NOT NULL DEFAULT 0, \
Total_Mobility REAL NOT NULL DEFAULT 0, \
Total_Exercise REAL NOT NULL DEFAULT 0, \
Total_Social_Hours REAL NOT NULL DEFAULT 0, \
Total_Sleep_1 REAL NOT NULL DEFAULT 0, \
Total_Sleep_2 REAL NOT NULL DEFAULT 0, \
Total_Sleep REAL NOT NULL DEFAULT 0, \
Total_Indulging REAL NOT NULL DEFAULT 0, \
Total_Flaking REAL NOT NULL DEFAULT 0, \
Total_Cursing REAL NOT NULL DEFAULT 0, \
Total_Intoxication REAL NOT NULL DEFAULT 0, \
Total_Vices REAL NOT NULL DEFAULT 0, \
Total_Burnout REAL NOT NULL DEFAULT 0, \
Total_Over_Extending REAL NOT NULL DEFAULT 0, \
Total_Quality_Of_Life REAL NOT NULL DEFAULT 0, \
Average_Project_Hours REAL NOT NULL DEFAULT 0, \
Average_Study_Hours REAL NOT NULL DEFAULT 0, \
Average_Administrative_Hours REAL NOT NULL DEFAULT 0, \
Average_Work REAL NOT NULL DEFAULT 0, \
Average_Strength_Training REAL NOT NULL DEFAULT 0, \
Average_Cardio REAL NOT NULL DEFAULT 0, \
Average_Mobility REAL NOT NULL DEFAULT 0, \
Average_Exercise REAL NOT NULL DEFAULT 0, \
Average_Social_Hours REAL NOT NULL DEFAULT 0, \
Average_Sleep_1 REAL NOT NULL DEFAULT 0, \
Average_Sleep_2 REAL NOT NULL DEFAULT 0, \
Average_Sleep REAL NOT NULL DEFAULT 0, \
Average_Indulging REAL NOT NULL DEFAULT 0, \
Average_Flaking REAL NOT NULL DEFAULT 0, \
Average_Cursing REAL NOT NULL DEFAULT 0, \
Average_Intoxication REAL NOT NULL DEFAULT 0, \
Average_Vices REAL NOT NULL DEFAULT 0, \
Average_Burnout REAL NOT NULL DEFAULT 0, \
Average_Over_Extending REAL NOT NULL DEFAULT 0, \
Average_Quality_Of_Life REAL NOT NULL DEFAULT 0 \
);"

create_log = "CREATE TABLE Burn_Log ( \
Date TEXT PRIMARY KEY NOT NULL, \
Description TEXT NOT NULL, \
Peak_Arousal REAL NOT NULL DEFAULT 1, \
Peak_Aggression REAL NOT NULL DEFAULT 1, \
Trigger_Thoughts TEXT NOT NULL, \
Result TEXT NOT NULL, \
Biofeedback_Filepath TEXT \
);"

create_factors = "CREATE TABLE Burn_Factors ( \
Date TEXT PRIMARY KEY NOT NULL, \
XXX INTEGER DEFAULT 0, \
Food INTEGER DEFAULT 0, \
Bread INTEGER DEFAULT 0, \
Cheese INTEGER DEFAULT 0, \
Sleep_Deprivation INTEGER DEFAULT 0, \
Noise INTEGER DEFAULT 0, \
Barking_Dog INTEGER DEFAULT 0, \
Media INTEGER DEFAULT 0, \
Social_Media INTEGER DEFAULT 0, \
People INTEGER DEFAULT 0, \
Crowds INTEGER DEFAULT 0, \
Traffic INTEGER DEFAULT 0, \
Hangover INTEGER DEFAULT 0, \
Other TEXT, \
Total_Factors INTEGER DEFAULT 0, \
FOREIGN KEY(Date) REFERENCES Burn_Log(Date) \
);"

create_psych = "CREATE TABLE Psych ( \
Date TEXT PRIMARY KEY NOT NULL, \
Type TEXT NOT NULL, \
Insight TEXT NOT NULL, \
Biofeedback_Filepath TEXT \
);"

insert_daily = "INSERT INTO Daily_Functionality (\
Weekday, Date, \
Project_Hours, Study_Hours, Administrative_Hours, Total_Work, \
Strength_Training, Cardio, Mobility, Total_Exercise, \
Social_Hours, Sleep_1, Sleep_2, Total_Sleep, \
Indulging, Flaking, Cursing, Intoxication, Total_Vices, \
Burnout, Quality_Of_Life\
) Values ("

insert_weekly = 'INSERT INTO Weekly_Functionality (\
Starting_Date, Ending_Date, \
Total_Project_Hours, Total_Study_Hours, Total_Administrative_Hours, Total_Work, \
Total_Strength_Training, Total_Cardio, Total_Mobility, Total_Exercise, \
Total_Social_Hours, Total_Sleep_1, Total_Sleep_2, Total_Sleep, \
Total_Indulging, Total_Flaking, Total_Cursing, Total_Intoxication, Total_Vices, \
Total_Burnout, Total_Quality_Of_Life\
) Values ("'

insert_monthly = 'INSERT INTO Monthly_Functionality (\
Starting_Date, Ending_Date, \
Average_Project_Hours, Average_Study_Hours, Average_Administrative_Hours, Average_Work, \
Average_Strength_Training, Average_Cardio, Average_Mobility, Average_Exercise, \
Average_Social_Hours, Average_Sleep_1, Average_Sleep_2, Average_Sleep, \
Average_Indulging, Average_Flaking, Average_Cursing, Average_Intoxication, Average_Vices, \
Average_Burnout, Average_Quality_Of_Life\
) Values ("'

insert_annually = 'INSERT INTO Annual_Functionality (\
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
) Values ("'

insert_burn_log = 'INSERT INTO Burn_Log (Date, Description, Peak_Arousal, Peak_Aggression, Trigger_Thoughts, Result) Values ("'

aggression_spinbox = """1: None
2: Muttering
3: Cursing
4: Screaming and Cursing
5: Rage Quitting
6: Veiled Threatening
7: Overt Threatening
8: Minor Violence
9: Moderate Violence
10: Extreme Violence
"""

energy_spinbox = """1: Barely awake
2: Calm
3: Focused
4: Mildly agitated
5: Moderately agitated
6: Very agitated
7: Between 6 & 8
8: Mild exertion
9: Moderate exertion
10: Heavy exertion
"""

keys = ['Total_Project_Hours',
    'Total_Study_Hours',
    'Total_Administrative_Hours',
    'Total_Work',
    'Total_Strength_Training',
    'Total_Cardio',
    'Total_Mobility',
    'Total_Exercise',
    'Total_Social_Hours', 
    'Total_Sleep_1', 
    'Total_Sleep_2', 
    'Total_Sleep', 
    'Total_Indulging', 
    'Total_Flaking', 
    'Total_Cursing', 
    'Total_Intoxication', 
    'Total_Vices',
    'Total_Burnout',
    'Total_Quality_Of_Life'
]

def ret_sums():
    sums = OrderedDict()
    # initialize each key/value pair with a value of 0:
    for k in keys:
        sums[k] = 0
    #
    return sums