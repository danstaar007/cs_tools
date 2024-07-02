
### add ssh server
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    Start-Service sshd
    Set-Service -Name sshd -StartupType 'Automatic'

### network drive and powershell
    type 'powershell' :)
    net use x: \\ip\working

### execution policy
    Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

### nano
    winget install GNU.Nano
        ### movement keys
            ^f, ^b, ^n, ^p 
                #### if not ssh
                    start nano (to open new win and keys should work)

