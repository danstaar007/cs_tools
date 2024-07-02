### mount cifs CLI
    sudo mount -t cifs //192.168.1.100/shared /mnt/smbshare -o username=johndoe,password=secret

### mount cifs fstab
    nano /etc/fstab
    //server/share /mnt/smbshare cifs credentials=/etc/smbcredentials,iocharset=utf8,sec=ntlm 0 0

### show dir total size in GB
    du -s --block-size=GB /var/log