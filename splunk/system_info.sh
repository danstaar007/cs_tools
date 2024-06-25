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
else
    vm="Physical Machine"
fi

IFS=$'\n'
printf "Hostname: $host_name\n"
printf "Host Type: $vm\n"
printf "Host S/N: $host_sn\n"

counter=1
for hdd in $hdds; do
    hdd_name=$(echo $hdd | awk '{print $1}')
    hdd_sn=$(echo $hdd | awk '{print $2}')
    printf "Hard Drive #$counter: $hdd_name\n"
    printf "Hard Drive #$counter S/N: $hdd_sn\n"
    printf "Hard Drive #$counter Vendor: " && cat "/sys/block/$hdd_name/device/model" && printf "\n"
    ((counter++))
done


unset IFS