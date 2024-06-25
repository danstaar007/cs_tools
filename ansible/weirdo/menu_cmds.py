import tkinter
import json
from tkinter import messagebox, Entry
import os
import platform

# Read the config.json file
with open('config.json', 'r') as f:
    config_vars = json.load(f)

os_name = platform.system()
#set db_path
if os_name == 'Windows':
    db_path = config_vars['Database Path (Win)']  
else:  
    db_path = config_vars['Database Path (Linux)']


def check_inventory():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the hosts from the database
    cursor.execute("SELECT hostname FROM hosts")
    hosts = cursor.fetchall()

    for host in hosts:
        hostname = host[0]
        inventory_file = f"{hostname}_inventory.json"

        # Check if the inventory file exists
        if not os.path.exists(inventory_file):
            # Query the operating system and save the live inventory file
            query_os_and_save_inventory(hostname, inventory_file)
        else:
            # Check the modification time of the inventory file
            modification_time = os.path.getmtime(inventory_file)
            modification_datetime = datetime.datetime.fromtimestamp(modification_time)
            current_datetime = datetime.datetime.now()

            # Check if the inventory file is older than 2 weeks
            if (current_datetime - modification_datetime).days > 14:
                # Re-query the operating system and replace the live inventory file
                query_os_and_save_inventory(hostname, inventory_file)

    conn.close()

def query_os_and_save_inventory(hostname, inventory_file):
    # Query the operating system and save the live inventory file
    if os_name == 'Windows':
        # Query Windows operating system
        inventory_data = query_windows_os(hostname)
    else:
        # Query Linux operating system
        inventory_data = query_linux_os(hostname)

    # Save the live inventory file
    with open(inventory_file, 'w') as f:
        json.dump(inventory_data, f)

def query_windows_os(hostname):
    # Query Windows operating system
    # Your code here
    pass

def query_linux_os(hostname):
    # Query Linux operating system
    # Your code here
    pass

