### This requires you to --> Settings --> Data inputs --> Forwarded inputs --> Scripts --> New remote Script
# Create a .bat that points to the script

##
# UF_host_fix.bat
# @echo off
# powershell.exe -ExecutionPolicy Bypass -File "%~dp0UF_host_fix.ps1"

### This section of the script is to correct the hostname on the UF in the event you have installed the UF but 
# later can't find the host.  Most likely DT has installed the UF with an old script and the server.conf
# contains the wrong hostname

### Get local host information
$splunk = "c:\program files\SplunkUniversalForwarder\etc\system\local"
$splunk_server = Select-String $splunk\server.conf -pattern "serverName = ([^$]+)" | Foreach-Object {$_.Matches} | Foreach-Object {$_.Groups[1].Value}

### Check local hostname against server.conf
if (-not ($splunk_server -eq $env:COMPUTERNAME)){
    $correct_servername="1"
} else {
    $correct_servername="0"
}

### Replace the incorrect hostname with the correct hostname in server.conf
if ($correct_servername -eq "1") {
    $server_conf="The hostname in server.conf is $splunk_server, which is incorrect. Overwriting server.conf with $env:COMPUTERNAME." 
    Copy-Item -Path "$splunk\server.conf" -Destination "$splunk\server_$(Get-Date -Format 'yyyyMMdd').conf.bak"
    (Get-Content -path $splunk\server.conf -Raw) -replace $splunk_server,$env:COMPUTERNAME | Set-Content $SPLUNK_LOCAL\server.conf
} else {
    $server_conf="The hostname in server.conf is the correct hostname, $splunk_server."
}

### This section of the script is to gather system information for the host to be used in the 'Metrics Dashboard'

### global
$global:bios_info=Get-WmiObject win32_bios
$host_name=$env:COMPUTERNAME

### Check for virtual machine
function is_virtual {
    $vm_type=@("VMware", "Virtual", "KVM", "Hyper-V", "VirtualBox", "QEMU")
    $computerSystem = Get-WmiObject Win32_ComputerSystem
    $bios_info = ($global:bios_info).Description
    $manufacturer = $computerSystem.Manufacturer
    $model = $computerSystem.Model

    foreach ($vm in $vm_type) {
        if ($bios_info -imatch $vm -or $manufacturer -imatch $vm -or $model -imatch $vm) {
            return $true
        } 
    }
    return $false
}
if (is_virtual) {
    $is_vm="Virtual Machine"
    $is_laptop="N/A"
} else {
    $is_vm="Physical Machine"
    $laptop=wmic systemenclosure get chassistypes

    if ($laptop -match "7" -or $laptop -match "8"-or $laptop -match "9"-or $laptop -match "13") {
        $is_laptop="Laptop"
    } else {
        $is_laptop="Workstation"
    }
}



### Get HDD serials
## NEEDS TO BE SAVED INTO AN ARRAY TO SHOW MULTIPLE HDDs
##############################

$disk_info = @()  # Initialize an empty array to store the custom objects

# Loop through each disk and capture the information in a custom object
foreach ($disk in Get-PhysicalDisk | Select-Object FriendlyName, Manufacturer, AdapterSerialNumber, Number) {
    [string]$name = $disk.FriendlyName
    [string]$type = $disk.Manufacturer
    [string]$hdd_sn = $disk.AdapterSerialNumber
    [int16]$hdd_num = $disk.Number

    # Create a custom object and add it to the array
    $disk_info += [pscustomobject]@{
        "HD_number" = $hdd_num
        "Type" = $type
        "Name" = $name
        "Serial Number" = $hdd_sn
    }
}

$hardDriveDetails = ($disk_info | ForEach-Object {
    "Hard Drive #$($_.HD_number): Type: $($_.Type), Name: $($_.Name), Serial Number: $($_.'Serial Number')"
}) -join "`n"


### Finished system info object
# Add the formatted disk information to the $system_info hashtable
$system_info = @{
    Hostname = $host_name
    "Hardware Type" = $is_VM
    "Machine S/N" = $global:bios_info.SerialNumber
    "Hard Drives" = $hardDriveDetails  # Consolidated hard drive information
    "Machine Type" = $is_laptop
    "UF config" = $server_conf
}

## VM vs Wprkstation :: label? Hardware Type
## Laptop vs Desktop :: label? Machine Type

# Output the system information for verification
$system_info.GetEnumerator() | ForEach-Object {
    if ($_.Key -eq "Hard Drives") {
        Write-Output "$($_.Key):"
        $_.Value -split "`n" | ForEach-Object {
            $driveDetails = $_ -split ", "
            # Extract and display the hard drive number
            $driveNumber = $driveDetails[0] -split ": "
            Write-Output "    $($driveNumber[0]):" # Hard Drive #X:
            
            # Correctly handle the 'Name' as 'Type' and other details
            foreach ($detail in $driveDetails) {
                $detailParts = $detail -split ": "
                if ($detailParts[0].Trim() -eq "Name") {
                    # Use 'Name' value as 'Type'
                    Write-Output "        Type: $($detailParts[1])"
                } elseif ($detailParts[0].Trim() -ne "" -and $detailParts[0].Trim() -notlike "Hard Drive #*") {
                    # For other details, display them normally, excluding the redundant line
                    Write-Output "        $($detailParts[0]): $($detailParts[1])"
                }
            }
            Write-Output "" # Add an empty line for readability between drives
        }
    } else {
        Write-Output "$($_.Key): $($_.Value)"
    }
}

#$system_info | ConvertTo-Json -Compress