

## win10,rhel9,dc-1

$paste_hosts = Read-Host "hostnames with commas"

$hnames = $paste_hosts -split ',' | ForEach-Object { $_.Trim() }

foreach ($hname in $hnames) {
    if (Test-Connection -ComputerName $hname -Count 1 -ErrorAction SilentlyContinue) {
        Write-Host "$hname is Online" -ForegroundColor Green
    }
    else {
        Write-Host "$hname is Offline" -ForegroundColor Red
    }
}

Read-Host "Press Enter to close"

