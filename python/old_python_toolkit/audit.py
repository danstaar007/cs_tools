# audit.py
import os
import subprocess
import pydoc
import threading
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform
from pathlib import Path

os_type = platform.system()
base_dir=" "

lock = threading.Lock()
thread_count = 0

def run_grep(index, pattern, file_pattern, extra_flags=[], post_process=None, description=None):
    global thread_count
    global base_dir

    search_pattern = os.path.join(base_dir, '**', file_pattern)
    files = glob.glob(search_pattern, recursive=True)

    if not files:
        return index, f"No files found for pattern: {search_pattern}"

    combined_output = ""
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {executor.submit(run_grep_on_file, file, pattern, extra_flags): file for file in files}
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                output = future.result()
            except Exception as exc:
                print(f'{file} generated an exception: {exc}')
            else:
                combined_output += output
    return index, combined_output, description

def run_grep_on_file(file, pattern, extra_flags):
    cmd = ['grep', '-i', pattern] + extra_flags + [file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout if result.returncode == 0 else result.stderr


def page_or_save(content, save_to_file=None):
    if save_to_file:
        with open(save_to_file, 'w') as f:
            f.write(content)
    else:
        pydoc.pager(content)

def exec_grep_commands(commands):
    global base_dir
    combined_output = ''
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_grep, index, **cmd): cmd for index, cmd in enumerate(commands)}
        
        for future in as_completed(futures):
            result = future.result()
            
            # Handle cases where run_grep returns 2 or 3 values
            if len(result) == 3:
                index, output, description = result
            else:
                index, output = result
                description = commands[index].get('description', f'Command {index + 1}')
                
            combined_output += f"========================================================================================================\n==============================> Results for {description} <==============================\n========================================================================================================\n\n{output}\n\n"

    return combined_output

def handle_output(combined_output):
    save_option = input("Do you want to save the output to a file? (y/n): ").strip().lower()
    if save_option == 'y':
        filename = input("Enter the filename: ").strip()
        page_or_save(combined_output, save_to_file=filename)
    else:
        page_or_save(combined_output)
    
def linux_audit():
    print(base_dir)
    combined_output = exec_grep_commands(commands)
    handle_output(combined_output)

def audit_menu():
    print("\n============== Manual Audit :( ===============") 
    print("*                                              *") 
    print("*               **** Linux ****                *") 
    print("* 1: Linux Manual Audit                        *")
    #print("* 2: Search for specific audit event (Linux)   *") 
    print("*                                              *")
   # print("*              **** Windows ****               *")    
   # print("* 3: Search for specific audit event (Windows) *")   
   # print("*                                              *")
    print("================================================")
    choice = input("--> ")
    if choice == '1':
        clear_screen()
        global base_dir 
        base_dir = input("Enter the base directory to search: ")
        linux_audit()

def clear_screen():
    if os_type == "Windows":
        os.system("cls")
    elif os_type == "Linux":
        os.system("clear")
    

commands = [
    {'pattern': 'unknown', 'file_pattern': '*secure*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'kill'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'user unknown', 'file_pattern': '*secure*', 'extra_flags': [], 'description': 'Finding cleartext passwords'},
    {'pattern': 'error', 'file_pattern': '*secure*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'failed: Address* | journal | No Such'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'bad password', 'file_pattern': '*secure*', 'extra_flags': ['-r'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'bad password', 'file_pattern': '*auth*', 'extra_flags': ['-r'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'unknown', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'kill'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'user unknown', 'file_pattern': '*auth*', 'extra_flags': [], 'description': 'Finding cleartext passwords'},
    {'pattern': 'retrieving', 'file_pattern': '*auth*', 'extra_flags': [], 'description': 'Finding cleartext passwords'},
    {'pattern': 'error', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'org.gtk.* | failed: Address* | journal: | No Such'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'USER', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'org.gtk.* | expire | journal | */bin/kill* | No Such'], 'description': 'Finding cleartext passwords'},
    {'pattern': 'error', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'org.gtk.* | failed: Address* | journal: | No Such'], 'description': 'Search for expired root passwords'},
    {'pattern': 'expired', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'timer'], 'description': 'Search for expired root passwords'},
    {'pattern': 'expire in', 'file_pattern': '*secure*', 'extra_flags': [], 'description': 'Search for expired root passwords'},
    {'pattern': 'command', 'file_pattern': '*secure*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'kill | nessus'], 'description': 'Find priv usage'},
    {'pattern': 'command', 'file_pattern': '*auth*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'kill | nessus'], 'description': 'Find priv usage'},
    #{'pattern': 'command', 'file_pattern': '*secure*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'CWD | EXECVE | USER* | LOGIN | clamscan | adjtimex | --- | uid=root | auid=unset | eggcups | firefox | nessus'], 'description': 'Find Security Relevant Object hits (SROs)'},
    {'pattern': 'su', 'file_pattern': '*secure*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'klocwork | such | csuser | Surrogate | error'], 'description': 'Search for switched users'},
    {'pattern': '*', 'file_pattern': '*reduced*', 'extra_flags': [], 'post_process': ['egrep', '-f', '-p', 'Xorg'], 'description': 'Find xorg'},
    {'pattern': 'EXECVE', 'file_pattern': '*reduced*', 'extra_flags': [], 'post_process': ['egrep', '-v', '-i', 'dzdo | key=priviledged | gvfs | gnome | pulse | ping | find | locate |finger |plugin-config | gconfd-2 | uid=root | utempter/utempter | */usr/sbin/sendmail* | nessus'], 'description': 'Find all commands excluding privileged commands'},
    {'pattern': '*', 'file_pattern': '*Audit_report_*', 'extra_flags': [], 'post_process': ['head', '-n', '100'], 'description': 'Commands ran, by who, when...'},
    {'pattern': '*', 'file_pattern': '*last*', 'extra_flags': [], 'post_process': ['head', '-n', '200'], 'description': 'Last logins'},
    
]
    
