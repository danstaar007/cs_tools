Function char($Array) {
    $Output = ""
    ForEach($chara in $Array){
        $Output += [char]$chara -join ""
    }
    Return $Output
}

$Monitor=Get-WmiObject WMIMonitorID -Namespace root\wmi

Char($Monitor.serialnumberid)