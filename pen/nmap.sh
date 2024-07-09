### get hostname
    nmap 10.129.121.188 -p445 -T5 -sV

### check if host is alive
    nmap 10.129.2.18 -sn -oA host 

### command to save output for later review
    nmap 10.129.2.0/24 -sn -oA FILENAME | grep for | cut -d" " -f5

### save the host list
    nmap -sn -oA tnet -iL hosts.lst | grep for | cut -d" " -f5

### connect scan / bypasses firewall / slow / completes 3-way handshake
    nmap 10.129.2.28 --disable-arp-ping -Pn -n -sT --reason

### if the hosts OS does not show
    nmap 10.129.2.18 -sn -oA host -PE --disable-arp-ping --reason

### check for UDP ports / slow / may not get response back unless application is instructed to from host
    nmap 10.129.2.28 -F -sU --reason

### get additional info
    nmap 192.168.1.112 -Pn -n --disable-arp-ping --reason -sV

    ### look at the TTL
        Windows: 128
        Linux: 64
        Cisco: 255
        Solaris: 255
        Mac OS X: 64

### There are a total of 6 different states for a scanned port we can obtain:
    open 	This indicates that the connection to the scanned port has been established. These connections can be TCP connections, UDP datagrams as well as SCTP associations.
    closed 	When the port is shown as closed, the TCP protocol indicates that the packet we received back contains an RST flag. This scanning method can also be used to determine if our target is alive or not.
    filtered 	Nmap cannot correctly identify whether the scanned port is open or closed because either no response is returned from the target for the port or we get an error code from the target.
    unfiltered 	This state of a port only occurs during the TCP-ACK scan and means that the port is accessible, but it cannot be determined whether it is open or closed.
    open|filtered 	If we do not get a response for a specific port, Nmap will set it to that state. This indicates that a firewall or packet filter may protect the port.
    closed|filtered 	This state only occurs in the IP ID idle scans and indicates that it was impossible to determine if the scanned port is closed or filtered by a firewall.

