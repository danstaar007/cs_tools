import tkinter as tk
from tkinter import messagebox


def new_file():
    #latest_table = db_manager.get_latest_table()
    pass

def save_file():
    pass

def exit_app(root):
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

def hide_menu(event):
    context_menu.unpost()

def bind_context_menu(Menu, frame, tree_fixed, tree_scrollable, root, edit_comments):
    global context_menu
    # Create a context menu
    context_menu = Menu(frame, tearoff=0)
    context_menu.add_command(label="Edit Comments", command=edit_comments)
    context_menu.add_command(label="View Findings", command=view_findings)
    context_menu.add_command(label="SSH", command=lambda: ssh_to_host(tree_fixed.item(tree_fixed.selection()[0], 'values')[1]))
    context_menu.add_command(label="Ping", command=lambda: ping_host(tree_fixed.item(tree_fixed.selection()[0], 'values')[1]))
    context_menu.add_command(label="Collect Logs", command=collect_logs)
    
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

def create_menubar(root, config_vars, edit_config):
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New Tracker", command=new_file)
    file_menu.add_command(label="Save and Clear", command=save_file)
    file_menu.add_command(label="Edit Configs", command=lambda: edit_config(config_vars))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: exit_app(root))
    menubar.add_cascade(label="File", menu=file_menu)

    software_menu = tk.Menu(menubar, tearoff=0)
    software_menu.add_command(label="Request SCR")
    software_menu.add_command(label="SCR Archive")
    software_menu.add_command(label="Live Inventory")
    software_menu.add_command(label="Compare Baseline")
    software_menu.add_command(label="Upload Baseline")
    menubar.add_cascade(label="Software", menu=software_menu)

    hardware_menu = tk.Menu(menubar, tearoff=0)
    hardware_menu.add_command(label="Request HCR")
    hardware_menu.add_command(label="HCR Archive")
    hardware_menu.add_command(label="Live Inventory")
    hardware_menu.add_command(label="Compare Baseline")
    hardware_menu.add_command(label="Upload Baseline")
    menubar.add_cascade(label="Hardware", menu=hardware_menu)

    ATC_menu = tk.Menu(menubar, tearoff=0)
    ATC_menu.add_command(label="Request Addition")
    ATC_menu.add_command(label="ATC Archive")
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
    sanitize_menu.add_command(label="Sanitization Archive")
    sanitize_menu.add_command(label="Awaiting Approval")
    sanitize_menu.add_command(label="Sanitized")
    menubar.add_cascade(label="Sanatization", menu=sanitize_menu)

    required_menu = tk.Menu(menubar, tearoff=0)
    required_menu.add_command(label="System Security Plan")
    required_menu.add_command(label="Deviations")
    required_menu.add_command(label="Audit Checklist")
    required_menu.add_command(label="DAC Form")
    required_menu.add_command(label="Backup Agreement")
    required_menu.add_command(label="ISCP (Contengency Plan)")
    required_menu.add_command(label="ISSO Appointment Record")
    menubar.add_cascade(label="Documentation", menu=required_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    joi_menu = tk.Menu(help_menu, tearoff=0)
    help_menu.add_cascade(label="JOI/WI", menu=joi_menu)
    joi_menu.add_command(label="Splunk")
    joi_menu.add_command(label="Nessus")
    joi_menu.add_command(label="SCAP")
    joi_menu.add_command(label="ISSO Queries")
    joi_menu.add_command(label="C3")
    joi_menu.add_command(label="Logcollector")
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="CSSOP")
    help_menu.add_command(label="RACI")
    help_menu.add_command(label="About")

    return menubar