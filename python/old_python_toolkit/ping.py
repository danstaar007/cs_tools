# ping.py
import subprocess
from threading import Thread, Lock
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

jobs = []
results = []
completed_jobs = 0  # Progress tracker
lock = Lock()  # Lock for thread-safe updates
os_type = platform.system()

# Ping function
def ping_hosts():
    single_host = input("Enter a single host (leave empty if using a host file): ")

    if single_host:
        hosts = [single_host]
    else:
        host_file = input("\nWhere is your hosts file located? ")
        try:
            with open(host_file, 'r') as f:
                hosts = f.readlines()
        except FileNotFoundError:
            print("File not found. Exiting...")
            exit(1)

    domains = ["district79.com", "fake.com", "work.com"]
    total_jobs = len(hosts) * len(domains)
    results = []

    # Initiate threads for multi 
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_fqdn = {}
        for domain in domains:
            print(f"Pinging hosts for {domain}")
            for r_host in hosts:
                fqdn = f"{r_host.strip()}.{domain}"
                future = executor.submit(ping_script, fqdn)
                future_to_fqdn[future] = fqdn

        completed_jobs = 0
        for future in as_completed(future_to_fqdn):
            completed_jobs += 1
            success, target = future.result()
            if target:
                results.append((success, target))
            print(f"Progress: {completed_jobs}/{total_jobs} jobs completed.")

        time.sleep(2)

        # Display results
        print("\nPingable hosts:")
        for success, target in results:
            if success:
                if os_type == "Linux":
                    print(f"\033[92m{target} is reachable.\033[0m")
                elif os_type == "Windows":
                    print(f"{target} is reachable.")

# Function to execute the ping
def ping_script(target):
    try:
        if os_type == "Linux":
            subprocess.run(["ping", "-c", "1", target], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True, target
        elif os_type == "Windows":
            result = subprocess.run(["powershell", "-Command", f"Test-Connection -ComputerName {target} -Count 1"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            if result.returncode == 0:
                return True, target
        return False, target
    except subprocess.CalledProcessError:
        return False, None