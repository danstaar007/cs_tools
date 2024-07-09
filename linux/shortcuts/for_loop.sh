#!/bin/bash

declare -A test=(
    [test_1]="1,2,3,4,5,6,7"
    [test_2]="1,2,3,4,5,6,7"
    )

for key in "${!test[@]}"; do
   #echo "${test[$key]}"
    echo "$key = ${test[$key]}"
done