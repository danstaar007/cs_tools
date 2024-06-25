### global
$global:bios_info=Get-WmiObject win32_bios
$global:machine_sn=''
$global:hdd_sn=get-physicaldisk | select AdapterSerialNumber
#$global:laptop=wmic systemenclosure get chassistypes

### Check for virtual machine
function is_virtual {
$vm_type=@("VMware", "Virtual", "KVM", "Hyper-V", "VirtualBox", "QEMU")
foreach ($vm in $vm_type) {
    if ($global:bios_info -match $vm) {
        return $true
        } 
    }
    return $false
}
$is_vm=if (is_virtual) {"VM"} else {"Physical"}

### Return some variables
function no_header {
    $global:machine_sn=($global:bios_info | Select-String -Pattern 'SerialNumber' -NotMatch) -replace '\s+', ''
    ## THIS SHOWS NOTHING // $global:hdd_sn=($global:hdd_sn | Select-String -Pattern 'AdapterSerialNumber' -NotMatch) -replace '\s+', ''
}

### Get HDD serials
$disk_info = foreach ($disk in Get-PhysicalDisk) {

[string]$name = $disk.FriendlyName
[string]$type = $disk.MediaType
[string]$hdd_sn = $disk.AdapterSerialNumber

    [pscustomobject]@{
    "Type"=$type;
    "Name"=$name;
    "Serial Number"=$hdd_sn;
    }
}

$machine_info = [pscustomobject]@{
	host=$env:COMPUTERNAME;
	type=$is_VM;
	machine_sn=$global:bios_info;
	}

### Finished system info object
$system_info = @{
    hostname=$env:COMPUTERNAME
	"Machine Type"=$is_VM
	machine_sn=$global:bios_info.SerialNumber
    hdd_vendor=$disk_info.Name
    hdd_type=$disk_info.Type
    hdd_serial=$disk_info.'Serial Number'.Trim()
}

#$system_info | ConvertTo-Json -Compress
$system_info 



### create a .bat with
#@echo off
#Powershell.exe -ExecutionPolicy remotesigned -File "%~dp0system_info.ps1"

### in .bat, check for PS, if no PS do this in CMD inside the .bat
