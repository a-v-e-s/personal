#!/bin/bash

mkdir -p Data/Biofeedback/
touch me.db

Command="CREATE TABLE Daily_Functionality (
    Date TEXT PRIMARY KEY NOT NULL,
    Weekday TEXT NOT NULL,
    Project_Hours REAL NOT NULL DEFAULT 0,
    Study_Hours REAL NOT NULL DEFAULT 0,
    Administrative_Hours REAL NOT NULL DEFAULT 0,
    Total_Work REAL NOT NULL DEFAULT 0,
    Strength_Training REAL NOT NULL DEFAULT 0,
    Cardio REAL NOT NULL DEFAULT 0,
    Mobility REAL NOT NULL DEFAULT 0,
    Total_Exercise REAL NOT NULL DEFAULT 0,
    Social_Hours REAL NOT NULL DEFAULT 0,
    Sleep_1 REAL NOT NULL DEFAULT 0,
    Sleep_2 REAL NOT NULL DEFAULT 0,
    Total_Replenishing REAL NOT NULL DEFAULT 0,
    Indulging REAL NOT NULL DEFAULT 0,
    Flaking REAL NOT NULL DEFAULT 0,
    Cursing REAL NOT NULL DEFAULT 0,
    Intoxication REAL NOT NULL DEFAULT 0,
    Total_Vices REAL NOT NULL DEFAULT 0,
    Burnout REAL NOT NULL DEFAULT 0,
    Over_Extending REAL NOT NULL DEFAULT 0,
    Quality_Of_Life REAL NOT NULL DEFAULT 0,
    Notes TEXT 
);"
sqlite3 me.db "$Command"

Command="CREATE TABLE Weekly_Functionality (
    Starting_Date TEXT PRIMARY KEY NOT NULL,
    Ending_Date TEXT NOT NULL,
    Total_Project_Hours REAL NOT NULL DEFAULT 0,
    Total_Study_Hours REAL NOT NULL DEFAULT 0,
    Total_Administrative_Hours REAL NOT NULL DEFAULT 0,
    Total_Work REAL NOT NULL DEFAULT 0,
    Total_Strength_Training REAL NOT NULL DEFAULT 0,
    Total_Cardio REAL NOT NULL DEFAULT 0,
    Total_Mobility REAL NOT NULL DEFAULT 0,
    Total_Exercise REAL NOT NULL DEFAULT 0,
    Total_Social_Hours REAL NOT NULL DEFAULT 0,
    Total_Sleep_1 REAL NOT NULL DEFAULT 0,
    Total_Sleep_2 REAL NOT NULL DEFAULT 0,
    Total_Replenishing REAL NOT NULL DEFAULT 0,
    Total_Indulging REAL NOT NULL DEFAULT 0,
    Total_Flaking REAL NOT NULL DEFAULT 0,
    Total_Cursing REAL NOT NULL DEFAULT 0,
    Total_Intoxication REAL NOT NULL DEFAULT 0,
    Total_Vices REAL NOT NULL DEFAULT 0,
    Total_Burnout REAL NOT NULL DEFAULT 0,
    Total_Over_Extending REAL NOT NULL DEFAULT 0,
    Total_Quality_Of_Life REAL NOT NULL DEFAULT 0
);"
sqlite3 me.db "$Command"

Command="CREATE TABLE Monthly_Functionality (
    Starting_Date TEXT PRIMARY KEY NOT NULL,
    Ending_Date TEXT NOT NULL,
    Average_Project_Hours REAL NOT NULL DEFAULT 0,
    Average_Study_Hours REAL NOT NULL DEFAULT 0,
    Average_Administrative_Hours REAL NOT NULL DEFAULT 0,
    Average_Work REAL NOT NULL DEFAULT 0,
    Average_Strength_Training REAL NOT NULL DEFAULT 0,
    Average_Cardio REAL NOT NULL DEFAULT 0,
    Average_Mobility REAL NOT NULL DEFAULT 0,
    Average_Exercise REAL NOT NULL DEFAULT 0,
    Average_Social_Hours REAL NOT NULL DEFAULT 0,
    Average_Sleep_1 REAL NOT NULL DEFAULT 0,
    Average_Sleep_2 REAL NOT NULL DEFAULT 0,
    Average_Replenishing REAL NOT NULL DEFAULT 0,
    Average_Indulging REAL NOT NULL DEFAULT 0,
    Average_Flaking REAL NOT NULL DEFAULT 0,
    Average_Cursing REAL NOT NULL DEFAULT 0,
    Average_Intoxication REAL NOT NULL DEFAULT 0,
    Average_Vices REAL NOT NULL DEFAULT 0,
    Average_Burnout REAL NOT NULL DEFAULT 0,
    Average_Over_Extending REAL NOT NULL DEFAULT 0,
    Average_Quality_Of_Life REAL NOT NULL DEFAULT 0
);"
sqlite3 me.db "$Command"

Command="CREATE TABLE Annual_Functionality (
    Starting_Date TEXT PRIMARY KEY NOT NULL,
    Ending_Date TEXT NOT NULL,
    Total_Project_Hours REAL NOT NULL DEFAULT 0,
    Total_Study_Hours REAL NOT NULL DEFAULT 0,
    Total_Administrative_Hours REAL NOT NULL DEFAULT 0,
    Total_Work REAL NOT NULL DEFAULT 0,
    Total_Strength_Training REAL NOT NULL DEFAULT 0,
    Total_Cardio REAL NOT NULL DEFAULT 0,
    Total_Mobility REAL NOT NULL DEFAULT 0,
    Total_Exercise REAL NOT NULL DEFAULT 0,
    Total_Social_Hours REAL NOT NULL DEFAULT 0,
    Total_Sleep_1 REAL NOT NULL DEFAULT 0,
    Total_Sleep_2 REAL NOT NULL DEFAULT 0,
    Total_Replenishing REAL NOT NULL DEFAULT 0,
    Total_Indulging REAL NOT NULL DEFAULT 0,
    Total_Flaking REAL NOT NULL DEFAULT 0,
    Total_Cursing REAL NOT NULL DEFAULT 0,
    Total_Intoxication REAL NOT NULL DEFAULT 0,
    Total_Vices REAL NOT NULL DEFAULT 0,
    Total_Burnout REAL NOT NULL DEFAULT 0,
    Total_Over_Extending REAL NOT NULL DEFAULT 0,
    Total_Quality_Of_Life REAL NOT NULL DEFAULT 0,
    Average_Project_Hours REAL NOT NULL DEFAULT 0,
    Average_Study_Hours REAL NOT NULL DEFAULT 0,
    Average_Administrative_Hours REAL NOT NULL DEFAULT 0,
    Average_Work REAL NOT NULL DEFAULT 0,
    Average_Strength_Training REAL NOT NULL DEFAULT 0,
    Average_Cardio REAL NOT NULL DEFAULT 0,
    Average_Mobility REAL NOT NULL DEFAULT 0,
    Average_Exercise REAL NOT NULL DEFAULT 0,
    Average_Social_Hours REAL NOT NULL DEFAULT 0,
    Average_Sleep_1 REAL NOT NULL DEFAULT 0,
    Average_Sleep_2 REAL NOT NULL DEFAULT 0,
    Average_Replenishing REAL NOT NULL DEFAULT 0,
    Average_Indulging REAL NOT NULL DEFAULT 0,
    Average_Flaking REAL NOT NULL DEFAULT 0,
    Average_Cursing REAL NOT NULL DEFAULT 0,
    Average_Intoxication REAL NOT NULL DEFAULT 0,
    Average_Vices REAL NOT NULL DEFAULT 0,
    Average_Burnout REAL NOT NULL DEFAULT 0,
    Average_Over_Extending REAL NOT NULL DEFAULT 0,
    Average_Quality_Of_Life REAL NOT NULL DEFAULT 0
);"
sqlite3 me.db "$Command"

Command="CREATE TABLE Burn_Log (
    Date TEXT PRIMARY KEY NOT NULL,
    Description TEXT NOT NULL,
    Peak_Arousal REAL NOT NULL DEFAULT 1,
    Peak_Aggression REAL NOT NULL DEFAULT 1,
    Pre_Existing_Stressors TEXT NOT NULL,
    Trigger_Thoughts TEXT NOT NULL,
    Result TEXT NOT NULL,
    Biofeedback_Filepath TEXT
);"
sqlite3 me.db "$Command"

Command="CREATE TABLE Psych (
    Date TEXT PRIMARY KEY NOT NULL,
    Type TEXT NOT NULL,
    Insight TEXT NOT NULL,
    Biofeedback_Filepath TEXT
);"
sqlite3 me.db "$Command"