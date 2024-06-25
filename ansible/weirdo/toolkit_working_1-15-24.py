import tkinter as tk
from tkinter import messagebox, ttk, Menu, font, Entry
import tkinter.simpledialog as tkSimpleDialog
import sqlite3
from sqlite3 import Error
import os
import platform
import subprocess
import json
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog
import json
import threading
import datetime

# Read the config.json file
with open('config.json', 'r') as f:
    config_vars = json.load(f)

os_name = platform.system()
root = tk.Tk()
root.title(config_vars['Window Title'])

#set db_path
if os_name == 'Windows':
    db_path = config_vars['Database Path (Win)']  
else:  
    db_path = config_vars['Database Path (Linux)']


def new_file():
    pass

def save_file():
    pass

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

def ssh_to_host(hostname):
   print(f"SSH to {hostname}")

def ping_host(hostname):
    print(f"Ping {hostname}")

def collect_logs():
    print("Collect Logs")

def view_findings():
    print("View Findings")

def scap_results():
    print("Scap Results")

def nessus_results():
    print("Nessus Results")

def conduct_c3():
    print("Conduct C3")

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

def save_config():
    config_vars['AD Servers'] = ad_servers_entry.get()
    config_vars['Database Path (Linux)'] = db_path_linux_entry.get()
    config_vars['Database Path (Win)'] = db_path_win_entry.get()
    config_vars['Window Title'] = window_title_entry.get()
    with open('config.json', 'w') as f:
        json.dump(config_vars, f)
    new_window.destroy()


def edit_config(config_vars):
    global ad_servers_entry, db_path_linux_entry, db_path_win_entry, window_title_entry, new_window
    new_window = tk.Toplevel()
    new_window.title('Configuration')
    new_window.geometry("400x300")

    # AD Servers
    ad_servers_label = tk.Label(new_window, text="AD Servers")
    ad_servers_label.grid(row=0, column=0, sticky="w")
    ad_servers_entry = tk.Entry(new_window)
    ad_servers_entry.grid(row=0, column=1)
    ad_servers_entry.insert(0, config_vars.get("AD Servers", ""))

    # Database Path (Linux)
    db_path_linux_label = tk.Label(new_window, text="Database Path (Linux)")
    db_path_linux_label.grid(row=1, column=0, sticky="w")
    db_path_linux_entry = tk.Entry(new_window)
    db_path_linux_entry.grid(row=1, column=1)
    db_path_linux_entry.insert(0, config_vars.get("Database Path (Linux)", ""))

    # Database Path (Win)
    db_path_win_label = tk.Label(new_window, text="Database Path (Win)")
    db_path_win_label.grid(row=2, column=0, sticky="w")
    db_path_win_entry = tk.Entry(new_window)
    db_path_win_entry.grid(row=2, column=1)
    db_path_win_entry.insert(0, config_vars.get("Database Path (Win)", ""))

    # Window Title
    window_title_label = tk.Label(new_window, text="Window Title")
    window_title_label.grid(row=3, column=0, sticky="w")
    window_title_entry = tk.Entry(new_window)
    window_title_entry.grid(row=3, column=1)
    window_title_entry.insert(0, config_vars.get("Window Title", ""))

    # Save button
    save_button = tk.Button(new_window, text="Save", command=save_config)
    save_button.grid(row=4, column=0, pady=10)

    # Cancel button
    cancel_button = tk.Button(new_window, text="Cancel", command=new_window.destroy)
    cancel_button.grid(row=4, column=1, pady=10)

def cancel():
    root.destroy()


def reload_treeview():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM findings")
        rows = cursor.fetchall()
        conn.close()

        for tree in [tree_fixed, tree_scrollable]:  
            for i in tree.get_children():
                tree.delete(i)

            for row in rows:
                status = ping_host(row[0])
                row = list(row)  
                row[1] = "✔" if row[1] == 1 else "✖"
                status = ping_host(row[0])
                if tree is tree_fixed:
                    tree.insert('', 'end', values=(status, row[0]))
                else:
                    tree.insert('', 'end', values=row[1:])
               
            # Update the Treeview widget
            tree.update_idletasks()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def update(hostname, column, entry):
    new_value = entry.get()
    # Update the database
    try:
        
        conn = sqlite3.connect(db_path) 
        cursor = conn.cursor()
        update_query = f"UPDATE findings SET {column} = ? WHERE hostname = ?" 
        cursor.execute(update_query, (new_value, hostname))
        # Commit the changes
        conn.commit()
    finally:
        # Close the connection
        if conn:
            conn.close()
    reload_treeview()

def update_status():
    global tree_fixed
    for child in tree_fixed.get_children():
        host = tree_fixed.set(child, "Hostname")
        thread = threading.Thread(target=update_host_status, args=(child, host))
        thread.start()
    root.after(10000, update_status)  # Schedule the function to run again after 10 secs

def update_host_status(child, host):
    status = ping_host(host)
    if status == "✔":
        root.after(0, lambda: tree_fixed.item(child, tags='online', values=(status, host)))
        root.after(0, lambda: tree_fixed.tag_configure('online', foreground='green'))
    else:
        root.after(0, lambda: tree_fixed.item(child, tags='offline', values=("✖", host)))
        root.after(0, lambda: tree_fixed.tag_configure('offline', foreground='red'))

def ping_host(host):
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 1 -w 1 {host} > nul 2>&1")
    else:
        response = os.system(f"ping -c 1 -W 1 {host} > /dev/null 2>&1")
    if response == 0:
        return "✔"  
    else:
        return "✖"  
    root.after(300000, lambda: ping_host(host))

def hide_menu(event):
    context_menu.unpost()

def edit_comments():
    if tree_fixed.selection():
        item_fixed = tree_fixed.selection()[0]
    else:
        print("No item selected in tree_fixed")
        return
    if tree_scrollable.selection():
        item_scrollable = tree_scrollable.selection()[0]
    else:
        print("No item selected in tree_scrollable")
        return
    # Get the hostname (key) from tree_fixed
    hostname = tree_fixed.set(item_fixed, "#2")
    value = tree_scrollable.set(item_scrollable, "#2")  

    # Create an Entry widget
    entry = Entry(tree_scrollable)
    entry.insert(0, value)
    x, y, width, height = tree_scrollable.bbox(item_scrollable, "#2")
    entry.place(x=x, y=y, width=width, height=height)

    column = "Comments" 

    def update_and_destroy(event):
        update(hostname, column, entry)
        if entry.winfo_exists():
            entry.destroy()

    entry.bind('<FocusOut>', update_and_destroy)
    entry.bind('<Return>', update_and_destroy)
    
    

def filter_treeview(tree, search_text, start_col, include_status):
    # Clear the treeview
    for i in tree.get_children():
        tree.delete(i)

    # Insert only the rows that contain the searched information
    for row in rows:
        if search_text.lower() in str(row).lower():
            row = list(row)  
            row[1] = "✔" if row[1] == 1 else "✖"
            if include_status:
                status = ping_host(row[0])
                tree.insert('', 'end', values=(status, *row[start_col:]))  # Include status
            else:
                tree.insert('', 'end', values=row[start_col:])  # Do not include status

def on_search(event):
    search_text = search_bar.get()
    # Filter both treeviews
    filter_treeview(tree_fixed, search_text, 0, True)  # Include status for fixed treeview
    filter_treeview(tree_scrollable, search_text, 1, False)  # Do not include status for scrollable treeview

def view_contents():
    create_gui()

def create_gui():
    global tree
    global frame
    top = root
    window_title = config_vars['Window Title']
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    top.geometry(f"{screen_width//2}x{screen_height//2}")

    style = ttk.Style()
    style.configure("Treeview", borderwidth=1, relief="solid")
    style.configure("Treeview.Heading", borderwidth=1, relief="solid")

    frame = tk.Frame(top)
    frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(frame, show='headings', style="Treeview")
    scroll_bar = ttk.Scrollbar(frame, orient='horizontal')
    tree.configure(xscrollcommand=scroll_bar.set)
    scroll_bar.configure(command=tree.xview)

    tree_fixed, tree_scrollable = create_treeviews()

    resize_columns()

    # Link the scrollbar to the scrollable Treeview
    tree_scrollable.configure(xscrollcommand=scroll_bar.set)
    scroll_bar.configure(command=tree_scrollable.xview)

    scroll_bar.pack(fill='x', side='bottom')
    tree_fixed.pack(side='left', fill='y')
    tree_scrollable.pack(side='left', fill='both', expand=True)
    
    bind_context_menu()

    update_status() 

def create_treeviews():
    global headers
    global tree_fixed
    global tree_scrollable
    headers = ("Ping", "Hostname","Logs Collected","Comments","Domain","Patch Date","IP","OS","OS Version","Uptime (secs)","Manufacturer","PC Name","Serial Number","VM","Network Devices","Drives Encrypted")
    tree["columns"] = headers

    style = ttk.Style()
    style.configure('Treeview', rowheight=25)

    # Create two Treeview widgets
    tree_fixed = ttk.Treeview(frame, columns=("Ping", "Hostname"), show='headings')
    tree_scrollable = ttk.Treeview(frame, columns=headers[2:], show='headings')

    for i, header in enumerate(headers):
        if header in ["Ping", "Hostname"]:
            tree_fixed.column(header, width=40, stretch=tk.NO, anchor='center')
            tree_fixed.heading(header, text=header, anchor='center')
        else:
            tree_scrollable.column(header, width=35, stretch=tk.NO, anchor='center')
            tree_scrollable.heading(header, text=header, anchor='center')

    return tree_fixed, tree_scrollable

def resize_columns():
    max_hostname_length = 0
    for row in rows:
        status = ping_host(row[0])
        row = list(row)  
        row[1] = "✔" if row[1] == 1 else "✖"
        status = ping_host(row[0])
        tree_fixed.insert('', 'end', values=(status, row[0]))
        tree_scrollable.insert('', 'end', values=row[1:])
        max_hostname_length = max(max_hostname_length, len(row[0]))

    tree_fixed.column('Hostname', width=font.Font().measure(max_hostname_length*'m'))

    # Resize the cells for the database content
    for i, col in enumerate(tree_scrollable['columns']):
        header_length = len(headers[i+2])
        max_content_length = max([len(str(tree_scrollable.set(child, col))) for child in tree_scrollable.get_children('')])
        max_length = max(header_length, max_content_length)
        max_length = min(max_length, 10)  # Do not exceed a width of 15
        tree_scrollable.column(col, width=font.Font().measure(max_length*'m'))

def bind_context_menu():
    global context_menu
    # Create a context menu
    context_menu = Menu(frame, tearoff=0)
    context_menu.add_command(label="Edit Comments", command=edit_comments)
    context_menu.add_command(label="SSH", command=lambda: ssh_to_host(tree_fixed.item(tree_fixed.selection()[0], 'values')[1]))
    context_menu.add_command(label="Ping", command=lambda: ping_host(tree_fixed.item(tree_fixed.selection()[0], 'values')[1]))
    context_menu.add_command(label="Collect Logs", command=collect_logs)
    context_menu.add_command(label="View Findings", command=view_findings)
    context_menu.add_command(label="Scap Results", command=scap_results)
    context_menu.add_command(label="Nessus Results", command=nessus_results)
    context_menu.add_command(label="Conduct C3", command=conduct_c3)

    def on_right_click(event):
        tree = event.widget
        # Get the ID of the selected item in this treeview
        selected_item = tree.identify_row(event.y)
        for t in [tree_fixed, tree_scrollable]:
            t.selection_set(selected_item)
        context_menu.post(event.x_root, event.y_root)
    for tree in [tree_fixed, tree_scrollable]:
        tree.bind("<Button-3>", on_right_click)
    root.bind("<Button-1>", hide_menu)

def fetch_rows():
    try:
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM findings")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

rows = fetch_rows()


def create_db():
    #password = tk.simpledialog.askstring("Password", "Enter password:", show='*')
    #become_pass = tk.simpledialog.askstring("Become Password", "Enter become password:", show='*')
    cmd = ["ansible-playbook", "-i", "new_hosts.ini", "facts.yaml", "-k", "--ask-become-pass"]
    env = os.environ.copy()
    #env["ANSIBLE_PASSWORD"] = password
    #env["ANSIBLE_BECOME_PASS"] = become_pass
    subprocess.run(cmd, env=env)
    view_contents() 
    create_db_button.destroy()

# Check if database connection exists
try:
   
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM findings")
    rows = cursor.fetchall()
except sqlite3.Error as e:
    create_db_button = tk.Button(root, text="Create DB File", command=create_db)
    create_db_button.pack(pady=20)

top_frame = tk.Frame(root)
top_frame.pack(side='top', fill='x')

## Menu
menubar = tk.Menu(top_frame)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Edit Configs", command=lambda: edit_config(config_vars))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

software_menu = tk.Menu(menubar, tearoff=0)
software_menu.add_command(label="Live Inventory")
software_menu.add_command(label="Compare Baseline")
software_menu.add_command(label="Upload Baseline")
menubar.add_cascade(label="Software", menu=software_menu)

hardware_menu = tk.Menu(menubar, tearoff=0)
hardware_menu.add_command(label="Live Inventory")
hardware_menu.add_command(label="Compare Baseline")
hardware_menu.add_command(label="Upload Baseline")
menubar.add_cascade(label="Hardware", menu=hardware_menu)

ATC_menu = tk.Menu(menubar, tearoff=0)
ATC_menu.add_command(label="Request Addition")
ATC_menu.add_command(label="Awaiting Config")
ATC_menu.add_command(label="Awaiting Validation")
menubar.add_cascade(label="ATC Queue", menu=ATC_menu)

network_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Network", menu=network_menu)

mobile_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Mobile", menu=mobile_menu)

metrics_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Metrics", menu=metrics_menu)

stasis_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Stasis", menu=stasis_menu)

sanitize_menu = tk.Menu(menubar, tearoff=0)
sanitize_menu.add_command(label="Request Sanitization")
sanitize_menu.add_command(label="Awaiting Approval")
sanitize_menu.add_command(label="Sanitized")
menubar.add_cascade(label="Sanatization", menu=sanitize_menu)

search_frame = tk.Frame(root)
search_frame.pack(side='top', fill='x')

# Configure the columns to distribute space evenly
search_frame.grid_columnconfigure(0, weight=1)
search_frame.grid_columnconfigure(2, weight=1)

# Place the search bar and label in the new frame
search_var = tk.StringVar()
search_label = tk.Label(search_frame, text="Search")
search_label.grid(row=0, column=1, padx=5, sticky='ew')  # Center the label
search_bar = tk.Entry(search_frame, textvariable=search_var)
search_bar.grid(row=0, column=2, padx=5, sticky='ew')  # Center the search bar
search_bar.bind('<Return>', on_search)


root.config(menu=menubar)
## End Menu

view_contents()

root.mainloop()
