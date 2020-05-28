#!/bin/bash

mkdir -p Data/Biofeedback/
touch me.db

# can i make this work instead??
#while read command; do
#    sqlite3 me.db $command
#done; < <(`python3 -c \
#"import src.statements as statements;
#print(statements.create_daily);
#print(statements.create_weekly);
#print(statements.create_monthly);
#print(statements.create_annually);
#print(statements.create_log);
#print(statements.create_factors);
#print(statements.create_psych);
#exit();"
#`)

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