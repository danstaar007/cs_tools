#!/bin/bash

### get the serverName from the server.conf
### other variables
server_conf="/opt/splunkforwarder/etc/system/local/server.conf"
server_hostname=$(cat "$server_conf" | grep "serverName =" | awk '{printf $3}')
host_name=$(hostname)

### check the server.conf serverName and replace the hostname if incorrect
### also backs up the serverName.conf
[[ "$server_hostname" != "$host_name" ]] && cp "$server_conf" "$server_conf".$(date +"%m%d%Y"); sed -i "s/$server_hostname/$host_name/" "$server_conf" 

