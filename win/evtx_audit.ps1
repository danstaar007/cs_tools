
clear-host
write-host "########################################################"
write-host "########## This is the EVTX file audit script ##########"
Write-host ""
write-host "########################################################"
write-host "" 
write-host ""
###
write-host "Enter the full folder path to audit"
write-host "If using the NetApp location, use '/net/netappxx/security/audit/'"
$audit_folder=(read-host ": ")

### array that holds the event codes and the description to display during the audit
# to add more event codes, add a new line at the bottom; ("eventcode 1", "eventcode 2 (if there is another code)"", "description")
$event_codes = @(
    ("4774", "", "An account was mapped for logon"),
    ("4775", "", "An account could not be mapped for logon"),
    ("4776", "", "The domain controller attempted to validate the credentials for an account"),
    ("4777", "", "The domain controller failed to validate the credentials for an account"),
    ("4741", "645", "A computer account was created"),
    ("4742", "646", "A computer account was changed"),
    ("4743", "646", "A computer account was deleted"),
    ("4782", "", "The password hash for an account was accessed"),
    ("4793", "", "The password policy checking API was called"),
    ("4727", "631", "A security-enabled global group was created"),
    ("4728", "632", "A member was added to a security-enabled global group"),
    ("4729", "633", "A member was removed from a security-enabled global group"),
    ("4730", "634", "A security-enabled global group was deleted"),
    ("4731", "635", "A security-enabled local group was created"),
    ("4732", "636", "A member was added to a security-enabled local group"),
    ("4733", "637", "A member was removed from a security-enabled local group"),
    ("4734", "638", "A security-enabled local group was deleted"),
    ("4735", "639", "A security-enabled local group was changed"),
    ("4737", "641", "A security-enabled global group was changed"),
    ("4754", "658", "A security-enabled universal group was created"),
    ("4755", "659", "A security-enabled universal group was changed"),
    ("4756", "660", "A member was added to a security-enabled universal group"),
    ("4757", "661", "A member was removed from a security-enabled universal group"),
    ("4758", "662", "A security-enabled universal group was deleted"),
    ("4764", "", "A group's type was changed"),
    ("4720", "624", "A user account was created"),
    ("4722", "626", "A user account was enabled"),
    ("4723", "627", "An attempt was made to change an account's password"),
    ("4724", "628", "An attempt was made to reset an account's password"),
    ("4725", "629", "A user account was disabled"),
    ("4726", "630", "A user account was deleted"),
    ("4738","", "A user account was changed"),
    ("4740", "644", "A user account was locked out"),
    ("4765", "", "SID History was added to an account"),
    ("4766", "", "An attempt was made to add SID History to an account"),
    ("4767", "", "A user account was unlocked"),
    ("4780", "", "The ACL was set on accounts which are members of administrators groups"),
    ("4781", "685", "The name of an account was changed"),
    ("4794", "", "An attempt was made to set the Directory Services Restore Mode"),
    ("5376", "", "Credential Manager credentials were backed up"),
    ("5377", "", "Credential Manager credentials were restored from a backup"),
    ("625", "", "User account type was changed"),
    ("4688", "", "A new process has been created"),
    ("4696", "", "A primary token was assigned to a process"),
    ("4662", "", "An operation was perfomed on an object"),
    ("0", "", "Screen pass logoff"),
    ("4634", "538", "An account was logged off"),
    ("4647", "551", "User initiated logoff"),
    ("1001", "", "Screen pass session locked"),
    ("1002", "", "Screen pass session unlocked"),
    ("1008", "", "Screen pass taken over"),
    ("1016", "", "Screen pass failure to take over session"),
    ("1064", "", "Screen pass session started"),
    ("1128", "", "Screen pass closed"),
    ("6424", "528", "An account was successfully logged on"),
    ("6425", "529", "An account was logged off"),
    ("6425", "539", "An account was logged off"),
    ("4648", "", "A logon was attempted using explicit credentials"),
    ("4675", "","SIDs were filtered"),
    ("540", "", "Successful network logon"),
    ("4964", "", "Special groups have been assigned to a new logon"),
    ("4656", "", "Handle Manipulation (failed object access)"),
    ("4664", "", "An attempt was made to create a hard link"),
    ("4985", "", "The state of a transaction has changed"),
    ("5051", "", "A file was virtualized"),
    ("560", "", "Faild object access"),
    ("4657", "", "A registry value was modified"),
    ("5039", "", "A registry key was virtualized"),
    ("4715", "", "The audit policy (SACL) on an object was changed"),
    ("4719", "612", "System audit policy was changed"),
    ("4817", "", "Auditing settings on an object were changed"),
    ("4902", "", "The per-user audit policy wtable was created"),
    ("4904", "", "An attempt was made to register a security event source"),
    ("4905", "", "An attempt was made to unregister a security event source"),
    ("4906", "", "The CrashOnAuditFail value has changed"),
    ("4907", "", "Auditing settings on an object were changed"),
    ("4908", "", "Special groups logon table modified"),
    ("4912", "", "Per user audit policy was changed"),
    ("4713", "", "Kerberos policy was changed"),
    ("4716", "", "Trusted domain information was modified"),
    ("4717", "", "Systemsecurity access was granted to an account"),
    ("4718", "", "System security access was removed from an account"),
    ("4739", "643", "Domain policy was changed"),
    ("4864", "", "A namespace collision was detected"),
    ("4865", "", "A trusted forest information entry was added"),
    ("4866", "", "A trusted forest information entry was removed"),
    ("4867", "", "A trusted forest information entry was modified"),
    ("4672", "", "Special privileges assigned to new logon"),
    ("4673", "", "A privileged service was called"),
    ("4674", "", "An operation was attempted on a privileged object"),
    ("4960", "", "IPSEC dropped an inbound packed that failed an integrity check"),
    ("4961", "", "IPSEC dropped an inbound packed that failed a replay check"),
    ("4962", "", "IPSEC dropped an inbound packed that failed a replay check (low sequence number)"),
    ("4963", "", "IPSEC dropped an inbound clear text packet that should have been secured"),
    ("4965", "", "IPSEC received a packet from a remote computer with an incorrect Security Parameter Index (SPI)"),
    ("5478", "", "IPSEC services has started successfully"),
    ("5479", "", "IPSEC services has been shutdown successfully"),
    ("5480", "", "IPSEC services failed to get the complete list of network interfaces on the computer"),
    ("5483", "", "IPSEC services fialed to initialize RPC server"),
    ("5484", "", "IPSEC services has experienced a critical failure and has been shut down"),
    ("5485", "", "IPSEC services failed to process some IPsec filters on a plug-and-play event for network interfaces"),
    ("4608", "512", "Windows is starting up"),
    ("4609", "513", "Windows is shutting down"),
    ("4616", "520", "The system time was changed"),
    ("4621", "", "Administrator recovered system from CrashOnAuditFail"),
    ("521", "", "Unable to log events to security log"),
    ("4610", "","An authentication package has been loaded by the local security authority"),
    ("4611", "", "A trusted logon process has been registered with the local security authority"),
    ("4614", "", "A notification package has been loaded by the security account manager"),
    ("4622" ,"", "A security package has been loaded by the local security auhority"),
    ("4697", "", "A service was installed in the system"),
    ("4612", "", "Internal resources allocated for the queuing of audit messages have been exuasted, leading to the loss of some audits"),
    ("4615", "", "Invalid use of LPC port"),
    ("4618", "", "A monitored security event pattern has occured"),
    ("4816", "", "RPC detected an integrity violation while decrypting an incoming message"),
    ("5038", "", "Code integrity determined that the image hash of a file is not valid"),
    ("5056", "", "A cryptgraphic self-test was performed"),
    ("5057", "", "A cryptographic primitive operation failed"),
    ("5060", "", "A cryptographic operation failed"),
    ("5061", "", "Cryptographic operation"),
    ("5062", "", "A kernel-mode cryptographice self-test was performed"),
    ("6281" ,"", "Code integrity determined that the page hashes of an image file are not valid"),
    ("19", "1022", "Patch installation activity"),
    ("1033", "", "Application installation activiy"),
    ("1102", "517", "Security event log was cleared"),
    ("1104", "", "Security log full"),
    ("1105", "", "Event log automatic backup"),
    ("4946", "", "A change has been made to windows firewall exception list; a rule was added"),
    ("4947", "", "A change has been made to windows firewall exception list; a rule was modified"),
    ("4948", "", "A change has been made to windows firewall exception list; a rule was deleted"),
    ("4954", "", "Windows firewall group policy settings has changed; a new setting has been applied"),
    ("851", "", "A change has been made to the windows firewall application exception list"),
    ("852", "", "A change has been made to the windows firewall port exception list"),
    ("854", "", "The windows firewall logging settings have changed"),
    ("4656", "", "NetApp open object"),
    ("4659", "", "NetApp open object with delete intent"),
    ("4663", "", "NetApp read/set/write object"),
    ("4670", "", "NetApppermissions or owner changed"),
    ("4719", "", "NetAppaudit policy changed"),
    ("4907", "", "NetApp auditing setting changed"),
    ("9999", "", "NetApp rename object")
)

### Add ability to filter by time as well

function audit_files($audit_file, $host_name) {
   # write-host $audit_file
    #write-host $host_name
    $Global:all_win_events = @()
    foreach ($event_code in $event_codes) {
        $eventcode_1 = $event_code[0]
        $eventcode_2 = $event_code[1]
        $description = $event_code[2]
        

        if ($eventcode_2 -eq "") {
            $result = Get-WinEvent -FilterHashtable @{ Path=$audit_file; Id=$eventcode_1 } -ErrorAction SilentlyContinue
        }
        else {
            $result = Get-WinEvent -FilterHashtable @{ Path=$audit_file; Id=($eventcode_1, $eventcode_2) } -ErrorAction SilentlyContinue
        }

        if ($result) {
            write-host "################################################################################################################"
            write-host "#     EventCode: $eventcode_1       EventCode:$eventcode_2"
            write-host "#     Description: $description"
            write-host "################################################################################################################"
            ($result | Select-Object TimeCreated, LogName, Id, UserName, MachineName, Message, ProccessId, LevelDisplayName | Out-Host)
            #foreach ($event in $Global:all_win_events) {
             #   Write-Host $event 
            #}
        }
    }
}

Get-ChildItem "$audit_folder"  | ForEach-Object {
    $evtx_file = $_.FullName
    $file_name = $_.Name -split ".evtx"
    
    audit_files $evtx_file $file_name
}
    
function pager($content) {
    $pageSize = [Math]::Max([Console]::WindowHeight - 1, 1)
    $currentPage = 0

    while ($true) {
        Clear-Host
        $startLine = $currentPage * $pageSize
        $endLine = $startLine + $pageSize - 1

        $content[$startLine..$endLine] | ForEach-Object {
            Write-Host $_
        }

        $key = $host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown').Character

        switch ($key) {
            'q' {
                return
            }
            ' ' {
                $currentPage++
                if ($currentPage * $pageSize -ge $content.Count) {
                    $currentPage = 0
                }
            }
            'b' {
                $currentPage--
                if ($currentPage -lt 0) {
                    $currentPage = [Math]::Ceiling($content.Count / $pageSize) - 1
                }
            }
            ':' {
                $searchTerm = Read-Host -Prompt 'Search term'
                $foundIndex = $content.IndexOf($searchTerm, $startLine)
                if ($foundIndex -ge 0) {
                    $currentPage = [Math]::Floor($foundIndex / $pageSize)
                }
            }
        }
    }
}

clear-host
if ($Global:all_win_events) {
    foreach ($event in $Global:all_win_events) {
        Write-Host $event 
    }
} else {
    Write-Host "No events found."
}








