def scap_results():
    print("Scap Results")

def nessus_results():
    print("Nessus Results")

def conduct_c3():
    print("Conduct C3")

    context_menu.add_command(label="Scap Results", command=scap_results)
    context_menu.add_command(label="Nessus Results", command=nessus_results)
    context_menu.add_command(label="Conduct C3", command=conduct_c3)