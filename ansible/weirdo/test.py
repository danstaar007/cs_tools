import os
import subprocess

def get_disk_info():
    if os.name == 'nt':  # For Windows
        cmd = 'wmic diskdrive get model,serialnumber'
    else:  # For Linux
        cmd = "lsblk -dno SERIAL,MODEL"

    output = subprocess.check_output(cmd, shell=True).decode()
    return output

print(get_disk_info())