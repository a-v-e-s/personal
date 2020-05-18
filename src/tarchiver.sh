#!/bin/bash

if [ $# -ne 2 || ! -d "$1" ]; then
    echo "Usage: `basename $0` <target-directory> <file-extension> [ <max-tar-age ] [ <max-tar-size-in-kb> ]"
    exit 1
elif [ `ls "$1"/*"$2" 2>/dev/null; echo $?` -eq 2 ]; then
    echo "No files found in $1 with extension $2"
    exit 2
fi

cd "$1"

FILE_EXTENSION="$2"
MAX_TARSIZE=10000 # KILOBYTES
SECONDS_PER_DAY=86400

get_crtime() {
    for target in "${@}"; do
        inode=$(stat -c %i "${target}")
        fs=`df  --output=source "${target}"  | tail -1`
        hextime=$(
            sudo debugfs -R 'stat <'"${inode}"'>' "${fs}" 2>/dev/null | 
            grep crtime: |
            egrep -o '[0-9a-f]{8}'|
            head -1 | 
            tr 'a-f' 'A-F'
        )
        crtime=`echo "ibase=16; $hextime" | bc`
        printf "%s" $crtime
    done
}


d=`date | cut -d ' ' -f2,3,4 | tr ' ' '_'`
nowtime=`date +%s`

cp me.db $d.$FILE_EXTENSION

if [ -z `ls *.tar 2>/dev/null` ]; then
    tar -cf recent.tar $d.db # create new tar file
elif [ `du recent.tar | cut -f1` -gt $MAX_TARSIZE || ]; then
