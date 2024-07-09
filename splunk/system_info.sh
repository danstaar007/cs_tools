#!/bin/bash

host_name=$(hostname)

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
