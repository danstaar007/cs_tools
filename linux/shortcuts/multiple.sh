#!/bin/bash

### if, then, else
    [[ "$server_hostname" = "$host_name" ]] && echo "is correct" || cp "$server_conf" "$server_conf".$(date +"%m%d%Y"); sed -i "s/$server_hostname/$host_name/" "$server_conf" 

### send multiple vars to a function
# create the function and use the $1, $2, $3 to pass the vars
# call the function with the vars in quotes
    function echo_vars() {
        echo "var1: $1"
        echo "var2: $2"
        echo "var3: $3"
    }
    echo_vars "use" "this" "to pass vars to functions"

