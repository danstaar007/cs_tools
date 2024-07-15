### nmap
    nmap -sCV xxx
        nmap -A -T5 -sV -sC -Pn -p- -oX NAME IP #--top-ports 1000
### use dirb to find hidden directories
    dirb http://xxx.htb /usr/share/wordlists/dirb/common.txt

### If port 80 is open and you get no website, add the ip and website to /etc/hosts
#   and look for subdomains
    ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/big.txt -u http://permx.htb/ -H "Host:FUZZ.permx.htb" -fw 20 -mc 200 -s  
        If you get a 200 response, add the ip and website to /etc/hosts

### use hydra to send user pass to web login
    hydra -l admin -P /usr/share/wordlists/rockyou.txt http://xxx.htb/login.php http-post-form "username=^USER^&password=^PASS^:Invalid username" -t 64 -w 30 -V
    hydra -l admin -P /usr/share/wordlists/rockyou.txt lms.permx.htb http-post-form "/index.php?:login=administrator&password=^PASS^:Login failed - incorrect login or password." -V    
        # initially try to login with the wrong password to see the error message
        # you may need to use developer console and look at the form to get the login paramters to see the POST/GET and look under 'requests' to find how they use username/pass. Could be 'login' 'pass'

### if that doesn't work... look at an exploit for the webapp.  The creator is likely at the bottom


