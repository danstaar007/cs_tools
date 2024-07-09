
### if, then, else
    [[ "$server_hostname" = "$host_name" ]] && echo "is correct" || cp "$server_conf" "$server_conf".$(date +"%m%d%Y"); sed -i "s/$server_hostname/$host_name/" "$server_conf" 

