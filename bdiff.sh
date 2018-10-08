#!/bin/bash

files=$(ls *.srt)

for list in $files
do
    files=$(ls *.srt | grep -v $list)
    for string in $(cat $list)
    do
        grep -q $string $files
        if [ $? -ne 0 ]
        then
           echo $string >> $list.uniq
        fi
    done
done
