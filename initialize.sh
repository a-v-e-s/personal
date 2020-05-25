#!/bin/bash

mkdir -p Data/Biofeedback/
touch me.db

Command=`python3 -c "import src.statements as statements; print(statements.create_daily)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_weekly)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_monthly)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_annually)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_log)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_factors)"`
sqlite3 me.db "$Command"

Command=`python3 -c "import src.statements as statements; print(statements.create_psych)"`
sqlite3 me.db "$Command"