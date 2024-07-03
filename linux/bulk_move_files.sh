#!/bin/bash

# array for each folder that needs to be moved and archived
# It works by adding (top level folder, mtime for days/ mmin for mins, 1st find mindepth, 1st find maxdepth, 2nd find mindepth, 2nd find maxdepth, destination folder)
# the intent is the top level folder contains the week folder of the month and year (top level)
# when archived, depending on the min/max depth, you will get different resulting naming conventions
# try to get the folder of the week to be the archived folder

# function to call after the find
# may be the way I am multi threading??
function tar_folder() {
    folder=$1
    tar --null -czf "$global_save_location/$archive" "$folder" && echo "$folder complete"
}

# array for each folder that needs to be moved and archived
# It works by adding (top level folder, mtime for days/ mmin for mins, 1st find mindepth, 1st find maxdepth, 2nd find mindepth, 2nd find maxdepth, destination folder)
# the intent is the top level folder contains the week folder of the month and year (top level)
# when archived, depending on the min/max depth, you will get different resulting naming conventions
# try to get the folder of the week to be the archived folder
declare -A locations=(
    ["location1"]="/linux/2024/04-01-20242024,mtime,2,2,0,2,60,/destination/folder"
   # ["location2"]="/linux/2024/04-01-20242024,mtime,2,2,0,2,60,/destination/folder"
   # ["location3"]="/linux/2024/04-01-20242024,mtime,2,2,0,2,60,/destination/folder"
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
    days_or_min="${params[5]}"
    days_old="${params[6]}"
    global_save_location=$"{key}"

    # start at base dir and find all files
    # the first two numbers in the array are used for this min/maxdepth (x,min, max, x, x,x)
   find "$top_level" -mindepth "$first_mindepth" -maxdepth "$first_maxdepth" -$days_or_min + $days_old -type d | while read base_name; do
        
        # Extract year and month for use when naming the TAR files
        # $archive_name is the ["location_x"] from the array
        year=$(basename "$(dirname "$base_name")")
        month=$(basename "$base_name")
        archive="$archive_name_${year}_${month}.tar.gz"

    # compress files older than 60 days and use the year and month to name the TAR files
    # if you are trying to test this on a local folder, make sure you change -mtime to -mmin for minutes in the array above.
    # make sure when testing you setup the folder structure exactly like the hierarchy you are executing this on.
    
    # this is the loop that create 6 jobs and waits until one becomes available to start the next
    # it calls the tar_folder function from above
    for folder in "$base_name"; do
        while (( $(jobs|wc -l) >=6 )); do
            sleep 1
        done
        echo "$folder archive started" 
        tar_folder "$folder" &
    done

    # WARNING!!! THIS WILL REMOVE THE ORGINAL FILES FROM THE ORIGINAL FILE LOCATION
    # removes the old files/folders from original location
    # uncomment the finds for this to work
    #find "$base_name" -type f -mtime +"$days_old" -exec rm {} +
    #find "$base_name" -mindepth 1 -type d -empty -delete

    done
done