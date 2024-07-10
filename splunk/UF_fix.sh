#!/bin/bash

### This script is to correct the hostname on the UF in the event you have installed the UF but 
# later can't find the host.  Most likely DT has installed the UF with an old script and the server.conf
# contains the wrong hostname


### get the serverName from the server.conf
# other variables
server_conf="/opt/splunkforwarder/etc/system/local/server.conf"
server_hostname=$(cat "$server_conf" | grep "serverName =" | awk '{printf $3}')
host_name=$(hostname)

### check the server.conf serverName and replace the hostname if incorrect
# also backs up the serverName.conf
[[ "$server_hostname" != "$host_name" ]] && cp "$server_conf" "$server_conf".$(date +"%m%d%Y"); sed -i "s/$server_hostname/$host_name/" "$server_conf"; server_host="The hostname in server.conf is $server_hostname, which is incorrect. Overwriting server.conf with $host_name."

[[ "$server_hostname" = "$host_name" ]] && server_host="The hostname in server.conf is correct, $server_hostname."

echo $server_host

