import os
import platform
from ping import ping_hosts, ping_script; from ad import query_ad; from audit import audit_menu ; from conmon import conmon
from check_forwarder import check_forwarder; from copy_files import copy_files; from fix_forwarder import fix_forwarder; from c3 import c3

# global
os_type = platform.system()

# Main Menu function
def show_menu():
    clear_screen()
    print("\n================== Main Menu ===================")
    print("* 1: Query Active Directory for devices        *")
    print("* 2: Ping host(s)                              *")
    print("* 3: Copy files from one host to another       *")
    print("* 4: Forwarder installed, version, server.conf *")
    print("* 5: Fix Forwarder                             *")
    print("* 6: C3 for Windows/Linux                      *")
    print("* 7: Manual Audit for Windows/Linux            *")
    print("* 8: CONMON                                    *")
    print("* Q: Quit                                      *")
    print("================================================\n")

def clear_screen():
    if os_type == "Windows":
        os.system("cls")
    elif os_type == "Linux":
        os.system("clear")

# Main loop
if __name__ == "__main__":
    while True:
        clear_screen()
        show_menu()
        print(" ")
        choice = input("--> ")
        if choice == '1':
            clear_screen()
            query_ad()
        elif choice == '2':
            clear_screen()
            ping_hosts()
        elif choice == '3':
            clear_screen()
            copy_files()
        elif choice == '4':
            clear_screen()
            check_forwarder()
        elif choice == '5':
            clear_screen()
            fix_forwarder()
        elif choice == '6':
            clear_screen()
            c3()
        elif choice == '7':
            clear_screen()
            audit_menu()
        elif choice == '8':
            clear_screen()
            conmon()
        elif choice.lower() == 'q':
            break
        print(" ")
        input("Press Enter to continue...")
