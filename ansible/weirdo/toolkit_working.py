import tkinter as tk
from tkinter import messagebox, ttk, Menu, font, Entry
import tkinter.simpledialog as tkSimpleDialog
import sqlite3
from sqlite3 import Error
import os
import platform
import subprocess

os_name = platform.system()

def new_file():
    # Add your logic here
    pass

def save_file():
    # Add your logic here
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

def update_status():
    global tree_fixed
    for child in tree_fixed.get_children():
        host = tree_fixed.set(child, "Hostname")
        status = ping_host(host)
        tree_fixed.set(child, "Ping", status)
        if status == "✔":
            tree_fixed.item(child, tags='online')
        else:
            tree_fixed.item(child, tags='offline')
    tree_fixed.tag_configure('online', foreground='green')
    tree_fixed.tag_configure('offline', foreground='red')
    root.after(5000, update_status)  # Schedule the function to run again after 5 secs

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
    # Get the selected item
    item = tree.selection()[0]

    # Get the hostname (key)
    hostname = tree.set(item, '#1')  # Replace '#1' with the actual column number of the hostname column

    # Get the current value of the comments column
    column = '#2'  # Replace '#3' with the actual column number of the comments column
    value = tree.set(item, column)

    # Create an Entry widget
    entry = Entry(tree)
    entry.insert(0, value)

    # Place the Entry widget over the cell
    x, y, width, height = tree.bbox(item, column)
    entry.place(x=x, y=y, width=width, height=height)

    # When the Entry widget loses focus or the Return key is pressed, update the Treeview and the database
    entry.bind('<FocusOut>', lambda event: update(hostname, column, entry))
    entry.bind('<Return>', lambda event: update(hostname, column, entry))

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
    global tree
    global tree_fixed
    global tree_scrollable
    global context_menu
    try:
            # Set the path to the SQLite database file
        if os_name == 'Windows':
            db_path = "H:\\dev\\git_repos\\snippets\\ansible\\toolkit\\output\\IS_hosts.db"  
        else:  
            db_path = "/home/hydr0burn@district79.com/dev/git_repos/snippets/ansible/toolkit/output/IS_hosts.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM findings")
        rows = cursor.fetchall()

        top = root
        top.title("Security Toolkit")
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

        # Insert rows and calculate max hostname length
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

        # Link the scrollbar to the scrollable Treeview
        tree_scrollable.configure(xscrollcommand=scroll_bar.set)
        scroll_bar.configure(command=tree_scrollable.xview)

        scroll_bar.pack(fill='x', side='bottom')
        tree_fixed.pack(side='left', fill='y')
        tree_scrollable.pack(side='left', fill='both', expand=True)
        
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

        # Bind the context menu to both treeviews
        for tree in [tree_fixed, tree_scrollable]:
            tree.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))
        #tree.bind('<Double-1>', open_command_prompt)
        
        root.bind("<Button-1>", hide_menu)

        update_status() 
    
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_db():
    password = tk.simpledialog.askstring("Password", "Enter password:", show='*')
    become_pass = tk.simpledialog.askstring("Become Password", "Enter become password:", show='*')
    cmd = ["ansible-playbook", "-i", "new_hosts.ini", "facts.yaml", "-k", "--ask-become-pass"]
    env = os.environ.copy()
    env["ANSIBLE_PASSWORD"] = password
    env["ANSIBLE_BECOME_PASS"] = become_pass
    subprocess.run(cmd, env=env)
    view_contents() 
    create_db_button.destroy()

root = tk.Tk()
root.title("Your Application")

# Check if database connection exists
try:
   # Set the path to the SQLite database file
    if os_name == 'Windows':
        db_path = "H:\\dev\\git_repos\\snippets\\ansible\\toolkit\\output\\IS_hosts.db"  
    else:  
        db_path = "/home/hydr0burn@district79.com/dev/git_repos/snippets/ansible/toolkit/output/IS_hosts.db"
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
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

config_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Configs", menu=config_menu)

network_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Network", menu=network_menu)

mobile_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Mobile", menu=mobile_menu)

metrics_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Metrics", menu=metrics_menu)

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
