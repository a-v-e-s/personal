#!/bin/bash

# We can't afford to let something go wrong
set -e

# Get the current date,
# name a copy of up-to-date file after it,
# and put the copy in the tar file:
today=`date +%Y-%m-%d`
cp me.db $today.db.bak
tar --append --file db.tar $today.db.bak
rm $today.db.bak

# if there are more than 10 files in the archive,
if [[ `tar --list --file db.tar | wc -l` -gt 10 ]]; then

    index=0
    declare -a timestamps
    while read i; do
        # get unix epoch seconds from date-string:
        c=`echo "$i" | cut -d '.' -f1`
        d=`date -d $c +%s`
        # timestamps is given values of "$unixtime:$filename"
        timestamps[$index]=$d:"$i"
        let index++
    done; < <(tar --list --file db.tar)

    # sort the array, cut to the first filename, and remove it
    sort < <(for value in "${timestamps[@]}"; do echo "$value"; done) | head -n 1 | cut -d ':' -f2 | xargs tar --delete --file db.tar 

fi

exit 0