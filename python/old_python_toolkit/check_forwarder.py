# check_forwarder.py
import subprocess
import getpass
import os

def check_forwarder():
    host = input("Enter a single host (leave empty if using a host file): ")

    if not host:
        host_file = input("\nWhere is your hosts file located? ")
        try:
            with open(host_file, 'r') as f:
                hosts = [line.strip() for line in f]
        except FileNotFoundError:
            print("File not found. Exiting...")
            exit(1)
    else:
        hosts = [host]

    username = getpass.getuser()
    password = getpass.getpass("Enter your password: ")
    # Get domain
    domain = os.getenv("USERDOMAIN")
    # for ssh creds
    ssh_username = f"{username}@{domain}.com"
    print(ssh_username)

    for host in hosts:
        print(f"Checking if Splunk Forwarder is installed on {host}...")

        try:
            # Try SSH first
            output = subprocess.check_output(["ssh", "-v","-o", "BatchMode=yes", "-o", "ConnectTimeout=5", f"{ssh_username}@{host}", "dpkg -l splunkforwarder"], text=True)
            print("Splunk Forwarder is installed.")
        except subprocess.CalledProcessError:
            try:
                # If SSH fails, try WinRM
                output = subprocess.check_output(["powershell", "-Command", f"$password = ConvertTo-SecureString '{password}' -AsPlainText -Force; $cred = New-Object System.Management.Automation.PSCredential('{username}', $password); Invoke-Command -ComputerName {host} -Credential $cred -ScriptBlock {{ Get-Service -Name SplunkForwarder }}"], stderr=subprocess.DEVNULL, text=True)
                if "Running" in output:
                    print("Splunk Forwarder is installed.")
                else:
                    print("Splunk Forwarder is not installed.")
            except subprocess.CalledProcessError:
                print(f"Could not connect to {host}.")
