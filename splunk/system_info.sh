#!/bin/bash

### This section of the script is to correct the hostname on the UF in the event you have installed the UF but 
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


### This section of the script is to gather system information for the host to be used with the 'Metrics Dashboard'

hdds=$(lsblk --nodeps -o name,serial -Sn /dev/sd* | awk '{$1=$1; print}')

is_vm=$(dmesg | grep "Hypervisor detected")
host_sn=$(lshw | grep -m1 'serial' | awk '{print $2}')

f_print () {
    echo $1 | awk $FORMAT $PRINTF
}

if [[ "$is_vm" == *"Hypervisor"* ]]; then
    vm="Virtual Machine"
    is_laptop="N/A"
else
    vm="Physical Machine"
    if ls /sys/class/power_supply/*/type 2> /dev/null | grep -q "Battery"; then
        is_laptop="Laptop"
    else
        is_laptop="Workstation"
    fi
fi




IFS=$'\n'
printf "Hostname: $host_name\n"
printf "Hardware Type: $vm\n"
printf "Machine S/N: $host_sn\n"
printf "Machine Type: $is_laptop\n"
printf "UF Config: $server_host\n"

echo "Hard Drives:"
for hdd in $hdds; do
    hdd_name=$(echo $hdd | awk '{print $1}')
    hdd_sn=$(echo $hdd | awk '{print $2}')
    hdd_type=$(cat "/sys/block/$hdd_name/device/type" 2>/dev/null || echo "Unknown Type")
    hdd_model=$(cat "/sys/block/$hdd_name/device/model" 2>/dev/null || echo "Unknown Model")
    
    echo "    Hard Drive #: $hdd_type"
    echo "        Type: $hdd_model"
    echo "        Serial Number: $hdd_sn"
    echo ""
done


unset IFS
