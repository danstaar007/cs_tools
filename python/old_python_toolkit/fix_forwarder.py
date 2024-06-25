# fix_forwarder.py

# Fix server.conf if wrong hostname or copy default inputs (populated from server) to local
# This will get the forwarder talking to the server
def fix_forwarder():
    print("\n1: Fix hostname in server.conf\n2: Copy default to local (if not seeing input on server)")  
    fix_option = input("\n---> ")