### This script is to correct the hostname on the UF in the event you have installed the UF but 
# later can't find the host.  Most likely DT has installed the UF with an old script and the server.conf
# contains the wrong hostname

### This requires you to --> Settings --> Data inputs --> Forwarded inputs --> Scripts --> New remote Script
# Create a .bat that points to the script

##
# UF_host_fix.bat
# @echo off
# powershell.exe -ExecutionPolicy Bypass -File "%~dp0UF_host_fix.ps1"


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
    #Write-output "The hostname in server.conf is $splunk_server, which is incorrect. Overwriting server.conf with $env:COMPUTERNAME." 
    Copy-Item -Path "$splunk\server.conf" -Destination "$splunk\server_$(Get-Date -Format 'yyyyMMdd').conf.bak"
    (Get-Content -path $splunk\server.conf -Raw) -replace $splunk_server,$env:COMPUTERNAME | Set-Content $SPLUNK_LOCAL\server.conf
} else {
    #Write-output "The hostname in server.conf is the correct hostname, $splunk_server."
}



