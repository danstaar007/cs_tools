import tkinter as tk
from tkinter import messagebox, ttk, Menu, font, Entry
import tkinter.simpledialog as tkSimpleDialog
import sqlite3
from sqlite3 import Error, Connection, Cursor
from contextlib import closing
import os
import platform
import subprocess
import json
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog
import json
import threading
import datetime
import re
from tk_menu_items import *
from button_cmds import *

# Read the config.json file
with open('config.json', 'r') as f:
    config_vars = json.load(f)

os_name = platform.system()
root = tk.Tk()
root.title(config_vars['IS_name'])

#set db_path
if os_name == 'Windows':
    db_path = config_vars['database_path_win']  
else:  
    db_path = config_vars['database_path_linux']

class DatabaseManager:
    def __init__(self, db_path, root):
        self.db_path = db_path
        self.root = root
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA cache_size=-32000")
        self.conn.execute("PRAGMA synchronous=full")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.execute("PRAGMA analysis_limit=400")
        self.conn.execute("PRAGMA optimize")
        self.conn.close()

    def get_all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        return tables

    def get_latest_table(self):
        tables = self.get_all_tables()
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        #is_tables = sorted([table[0] for table in tables if re.match(fr'ISxxxx_{date_str}', table[0])], reverse=True)
        is_tables = sorted([table[0] for table in tables if re.match(fr'ISxxxx', table[0])], reverse=True)
        return is_tables[0] if is_tables else None

    def fetch_rows(self):
        latest_table = self.get_latest_table()

        if latest_table is not None:
            self.cursor.execute(f"SELECT * FROM {latest_table}")
            rows = self.cursor.fetchall()
            return rows
        else:
            return ["bad table"]

    def update(self, table_name, hostname, column, entry):
        new_value = entry.get()
        def update_db():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            try:
                update_query = f"UPDATE {table_name} SET {column} = ? WHERE hostname = ?" 
                cursor.execute(update_query, (new_value, hostname))
                conn.commit()
            finally:
                conn.close()
                self.root.after(0, reload_treeview)
        threading.Thread(target=update_db).start()

    def process_ping(self, tree, tree_fixed):
        latest_table = self.get_latest_table()
        if latest_table is not None:
            rows = self.fetch_rows() 
            for row in rows:
                status = ping_host(row[0])
                row = list(row)  
                row[1] = "✔" if row[1] == 1 else "✖"
                status = ping_host(row[0])
                if tree is tree_fixed:
                    tree.insert('', 'end', values=(status, row[0]))
                else:
                    tree.insert('', 'end', values=row[1:])

    def fetch_domains(self):
        latest_table = self.get_latest_table()
        if latest_table is not None:
            self.cursor.execute(f"SELECT domain FROM {latest_table}")
            domains = self.cursor.fetchall()
            return domains
        else:
            return ["No table"]
    
    def fetch_os(self):
        latest_table = self.get_latest_table()
        if latest_table is not None:
            self.cursor.execute(f"SELECT os FROM {latest_table}")
            os_data = self.cursor.fetchall()
            return os_data
        else:
            return ["No table"]

db_manager = DatabaseManager(db_path, root)
rows = db_manager.fetch_rows()

def save_config():
    config_vars['AD_servers'] = ad_servers_entry.get()
    config_vars['database_path_linux'] = db_path_linux_entry.get()
    config_vars['database_path_win'] = db_path_win_entry.get()
    config_vars['IS_name'] = window_title_entry.get()
    config_vars['splunk_server'] = splunk_server_entry.get()
    config_vars['playbook_location'] = playbook_entry.get()
    config_vars['ansible_machine'] = ansible_entry.get()
    with open('config.json', 'w') as f:
        json.dump(config_vars, f)
    new_window.destroy()

def edit_config(config_vars):
    global ad_servers_entry, db_path_linux_entry, db_path_win_entry, window_title_entry, new_window, winuser_entry, splunk_server_entry, playbook_entry
    new_window = tk.Toplevel()
    new_window.title('Configuration')
    new_window.geometry("600x400")
    # Make the second column expandable
    new_window.grid_columnconfigure(1, weight=1)
    new_window.grid_columnconfigure(2, weight=1, minsize=10)
    # AD Servers
    ad_servers_label = tk.Label(new_window, text="AD Servers")
    ad_servers_label.grid(row=0, column=0, sticky="w", padx=2)
    ad_servers_entry = tk.Entry(new_window)
    ad_servers_entry.grid(row=0, column=1, sticky="ew")
    ad_servers_entry.insert(0, config_vars.get("AD_servers", ""))
    # Database Path (Linux)
    db_path_linux_label = tk.Label(new_window, text="Database Path (Linux)")
    db_path_linux_label.grid(row=1, column=0, sticky="w", padx=2)
    db_path_linux_entry = tk.Entry(new_window)
    db_path_linux_entry.grid(row=1, column=1, sticky="ew")
    db_path_linux_entry.insert(0, config_vars.get("database_path_linux", ""))
    # Database Path (Win)
    db_path_win_label = tk.Label(new_window, text="Database Path (Win)")
    db_path_win_label.grid(row=2, column=0, sticky="w", padx=2)
    db_path_win_entry = tk.Entry(new_window)
    db_path_win_entry.grid(row=2, column=1, sticky="ew")
    db_path_win_entry.insert(0, config_vars.get("database_path_win", ""))
    # Window Title
    window_title_label = tk.Label(new_window, text="IS Name")
    window_title_label.grid(row=3, column=0, sticky="w", padx=2)
    window_title_entry = tk.Entry(new_window)
    window_title_entry.grid(row=3, column=1, sticky="ew")
    window_title_entry.insert(0, config_vars.get("IS_name", ""))
    # Splunk Server
    splunk_server_label = tk.Label(new_window, text="Splunk Server")
    splunk_server_label.grid(row=4, column=0, sticky="w", padx=2)
    splunk_server_entry = tk.Entry(new_window)
    splunk_server_entry.grid(row=4, column=1, sticky="ew")
    splunk_server_entry.insert(0, config_vars.get("splunk_server",""))
    # Playbook Location
    playbook_label = tk.Label(new_window, text="Playbook Location")
    playbook_label.grid(row=5, column=0, sticky="w", padx=2)
    playbook_entry = tk.Entry(new_window)
    playbook_entry.grid(row=5, column=1, sticky="ew")
    playbook_entry.insert(0, config_vars.get("playbook_location",""))
    # Windows User (To elevate)
    winuser_label = tk.Label(new_window, text="Windows User")
    winuser_label.grid(row=6, column=0, sticky="w", padx=2)
    winuser_entry = tk.Entry(new_window)
    winuser_entry.grid(row=6, column=1, sticky="ew")
    winuser_entry.insert(0, config_vars.get("Windows User",""))
    # Ansible Machine (Delegate)
    ansible_label = tk.Label(new_window, text="Ansible Machine")
    ansible_label.grid(row=7, column=0, sticky="w", padx=2)
    ansible_entry = tk.Entry(new_window)
    ansible_entry.grid(row=7, column=1, sticky="ew")
    ansible_entry.insert(0, config_vars.get("ansible_machine",""))

    # Save button
    save_button = tk.Button(new_window, text="Save", command=save_config)
    save_button.grid(row=8, column=0, pady=10)

    # Cancel button
    cancel_button = tk.Button(new_window, text="Cancel", command=new_window.destroy)
    cancel_button.grid(row=8, column=1, pady=10)

def cancel():
    root.destroy()

def reload_treeview():
    try:
        for tree in [tree_fixed, tree_scrollable]:  
            for i in tree.get_children():
                tree.delete(i)
            db_manager.process_ping(tree, tree_fixed) 
            tree.update_idletasks()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def update(hostname, column, entry):
    latest_table = db_manager.get_latest_table()
    if latest_table is not None:
        db_manager.update(latest_table, hostname, column, entry)
    else:
        print("No table found.")

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
        if tree_fixed.exists(child):
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

def sync_scroll(event):
    tree_fixed.yview_scroll(-1*(event.delta//120), 'units')
    tree_scrollable.yview_scroll(-1*(event.delta//120), 'units')

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

def create_gui():
    global tree
    global frame
    top = root
    window_title = config_vars['IS_name']
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
    
    bind_context_menu(Menu, frame, tree_fixed, tree_scrollable, root, edit_comments)

    tree_fixed.bind('<MouseWheel>', sync_scroll)
    tree_scrollable.bind('<MouseWheel>', sync_scroll)

    update_status() 

def create_treeviews():
    global headers
    global tree_fixed
    global tree_scrollable
    headers = ("Ping", "Hostname","Logs Collected","Comments","Domain","Patch Date","IP","OS","OS Version","Build","Local Accounts", "Device Control" , "CDROM", "Uptime (secs)","Manufacturer","PC Name","Serial Number","VM","Network Devices","Drives Encrypted")
    tree["columns"] = headers

    style = ttk.Style()
    style.configure('Treeview', rowheight=25)

    # Create two Treeview widgets
    tree_fixed = ttk.Treeview(frame, columns=("Ping", "Hostname"), show='headings')
    tree_scrollable = ttk.Treeview(frame, columns=headers[2:], show='headings')

    for i, header in enumerate(headers):
        if header in ["Ping", "Hostname"]:
            tree_fixed.column(header, width=40, stretch=tk.NO, anchor='center')
            tree_fixed.heading(header, text=header, anchor='center', command=lambda _col=header: sort_column(tree_fixed, tree_scrollable, _col, False))
        else:
            tree_scrollable.column(header, width=35, stretch=tk.NO, anchor='center')
            tree_scrollable.heading(header, text=header, anchor='center', command=lambda _col=header: sort_column(tree_scrollable, tree_fixed, _col, False))

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

def sort_column(tv1, tv2, col, reverse):
    l = [(tv1.set(k, col), k) for k in tv1.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv1.move(k, '', index)
        tv2.move(k, '', index)

    # reverse sort next time
    tv1.heading(col, command=lambda: sort_column(tv1, tv2, col, not reverse))
    tv2.heading("#0", command=lambda: sort_column(tv2, tv1, "#0", not reverse))

def create_db():
    #password = tk.simpledialog.askstring("Password", "Enter password:", show='*')
    #become_pass = tk.simpledialog.askstring("Become Password", "Enter become password:", show='*')
    cmd = ["ansible-playbook", "-i", "new_hosts.ini", "facts.yaml", "-k", "--ask-become-pass"]
    env = os.environ.copy()
    #env["ANSIBLE_PASSWORD"] = password
    #env["ANSIBLE_BECOME_PASS"] = become_pass
    subprocess.run(cmd, env=env)
    create_gui() 
    create_db_button.destroy()

# Check if database connection exists
# try:
   
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM findings")
#     rows = cursor.fetchall()
#     view_contents()
# except sqlite3.Error as e:
#     create_db_button = tk.Button(root, text="Create DB File", command=create_db)
#     create_db_button.pack(pady=20)

top_frame = tk.Frame(root)
top_frame.pack(side='top', fill='x')

## Menu

menubar = create_menubar(root, config_vars, edit_config)
root.config(menu=menubar)

# Search bar and buttons
search_frame = tk.Frame(root)
search_frame.pack(fill='x')

tracker_button = tk.Button(search_frame, text="Audit Tracker")
tracker_button.pack(side='left', padx=2, pady=5)
collect_button = tk.Button(search_frame, text="Logcollect", command=collect_logs)
collect_button.pack(side='left', padx=2, pady=5)
#SCR_button = tk.Button(search_frame, text="SCR Tracker")
#SCR_button.pack(side='left', padx=2, pady=5)
#HCR_button = tk.Button(search_frame, text="HCR Tracker")
#HCR_button.pack(side='left', padx=2, pady=5)
downed_button = tk.Button(search_frame, text="Downed 2+ Hours")
downed_button.pack(side='left', padx=2, pady=5)
splunk_button = tk.Button(search_frame, text="Not in Splunk")
splunk_button.pack(side='left', padx=2, pady=5)
forwarder_button = tk.Button(search_frame, text="Bad Forwarders")
forwarder_button.pack(side='left', padx=2, pady=5)
playbook_button = tk.Button(search_frame, text="Playbooks")
playbook_button.pack(side='left', padx=2, pady=5)

# Fetch the domain data
domains = db_manager.fetch_domains()
domains = list(set(item for sublist in domains for item in sublist))
domains.append('All Domains')
domain_var = tk.StringVar()
domain_combobox = ttk.Combobox(search_frame, textvariable=domain_var, values=domains)
domain_combobox.pack(side='left', padx=8)

domain_var.set('All Domains')

def on_domain_selected(event):
    search_text = domain_var.get()
    if search_text == 'All Domains':
        search_text = ''  
    filter_treeview(tree_fixed, search_text, 0, True)  # Include status for fixed treeview
    filter_treeview(tree_scrollable, search_text, 1, False)  # Do not include status for scrollable treeview

domain_combobox.bind('<<ComboboxSelected>>', on_domain_selected)

# Fetch the operating system data
os_data = db_manager.fetch_os()  # Replace with your function to fetch OS data
os_data = list(set(item for sublist in os_data for item in sublist))
os_data.append('All Operating Systems')

os_var = tk.StringVar()
os_combobox = ttk.Combobox(search_frame, textvariable=os_var, values=os_data)
os_combobox.pack(side='left', padx=8)

os_var.set('All Operating Systems')

def on_os_selected(event):
    search_text = os_var.get()
    if search_text == 'All Operating Systems':
        search_text = ''  
    filter_treeview(tree_fixed, search_text, 0, True)  # Include status for fixed treeview
    filter_treeview(tree_scrollable, search_text, 1, False)  # Do not include status for scrollable treeview

os_combobox.bind('<<ComboboxSelected>>', on_os_selected)

# Place the search bar and label in the new frame
search_var = tk.StringVar()
search_label = tk.Label(search_frame, text="Search")
search_label.pack(side='left', padx=5)
search_bar = tk.Entry(search_frame, textvariable=search_var)
search_bar.pack(side='left', fill='x', expand=True, padx=5)
search_bar.bind('<Return>', on_search)

root.config(menu=menubar)




## End Menu

create_gui()

root.mainloop()
