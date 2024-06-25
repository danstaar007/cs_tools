# ad.py
import os
import subprocess
import platform
import csv

# Function to query Active Directory for devices
# I want to CLI "splunk seary ' | metadata type=hosts index=*' -auth "username:password -output csv > splunk_hosts.csv"
# Figuring out how to protect password which will help out with SSH stuff as well 

os_type = platform.system()

def query_ad():
    csv_filename = 'ad_computers.csv'
    
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Enabled']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        if os_type == "Windows":
            try:
                ad_host = input("Enter your domain controller hostname: ")
                cmd = ["powershell", "-Command", f"Invoke-Command -ComputerName {ad_host} -ScriptBlock {{ Get-ADComputer -Filter * | Select-Object Name, Enabled }}"]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                print(f"Command Output: {result.stdout}")
                print(f"Command Error: {result.stderr}")

###### CAN"T GET TO WORK YET
                """ if result.returncode == 0:
                    lines = result.stdout.strip().split("\r\n")[2:]
                    entry = {}
                    for line in lines:
                        if ": " in line:
                            key, value = [x.strip() for x in line.split(": ", 1)]
                            if key == "Name" or key == "Enabled":
                                entry[key] = value
                        if "Name" in entry and "Enabled" in entry:
                            writer.writerow({'Name': entry['Name'], 'Enabled': entry['Enabled']})
                            entry = {}
                    print(f"AD computers written to {csv_filename}")
                else:
                    print(f"Command failed with error code {result.returncode}")
                """
            except Exception as e:
                print(f"Error: {e}") 


        elif os_type == "Linux":
           print("\nThis function is only available on Windows PowerShell :(")

    # Open the CSV file with the default application
    if os_type == "Windows":
        os.system(f"start {csv_filename}")
    else:
        pass
