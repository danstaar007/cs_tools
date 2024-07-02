#!/bin/bash

# array for each folder that needs to be moved and archived
# It works by adding (top level folder,1st find mindepth, 1st find maxdepth, 2nd find mindepth, 2nd find maxdepth)
# the intent is the top level folder contains the week folder of the month and year (top level)
# when archived, depending on the min/max depth, you will get different resulting naming conventions
# try to get the folder of the week to be the archived folder

declare -A locations=(
    ["location1"]="/linux/2024/04-01-20242024,0,1,1,1,60"
    ["location2"]="/domain_folder/2024/04-01-2024,0,2,1,2,60"
    ["location3"]="/domain_folder/2023/04-01-2023,0,2,1,2,60"
    # Add more locations as needed
)

# this loops through the array and creates the values for the commands below
for key in "${!locations[@]}"; do
    IFS=',' read -r -a params <<< "${locations[$key]}"
    top_level="${params[0]}"
    first_mindepth="${params[1]}"
    first_maxdepth="${params[2]}"
    second_mindepth="${params[3]}"
    second_maxdepth="${params[4]}"
    days_old="${params[5]}"

    # start at base dir and find all files
    # the first two numbers in the array are used for this min/maxdepth (x,min, max, x, x,x)
   find "$top_level" -mindepth "$first_mindepth" -maxdepth "$first_maxdepth" -type d | while read base_name; do
        
        # Extract year and month for use when naming the TAR files
        year=$(basename "$(dirname "$base_name")")
        month=$(basename "$base_name")
        archive="${year}_${month}.tar.gz"

    # compress files older than 60 days and use the year and month to name the TAR files
    # if you are trying to test this on a local folder, instead of -mtime, use -mmin for minutes.
    # make sure when testing you setup the folder structure exactly like the hierarchy you are executing this on.
    
    # the second two numbers in the array are used for this min/maxdepth (x,min, max, x, x,x)
    find "$base_name" -type f -mtime +"$days_old" -mindepth "$second_mindepth" -maxdepth "$second_maxdepth" -print0 | tar --null --directory="$(dirname "$base_name")" -czvf "/working/test_move/$archive" --transform "s,^$month,$year/$month," --files-from -
        
    # removes the old files/folders from original location
    find "$base_name" -type f -mtime +"$days_old" -exec rm {} +
    find "$base_name" -mindepth 1 -type d -empty -delete

    done
done