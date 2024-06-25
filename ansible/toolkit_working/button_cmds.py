import subprocess

def collect_logs():
    playbook_path = "/path/to/your/playbook.yml"
    inventory_file = "/path/to/your/hosts.ini"
    limit_file = "/path/to/your/collect_logs.txt"
    command = ["ansible-playbook", "-i", inventory_file, "-l", limit_file, playbook_path]
    subprocess.run(command, check=True)