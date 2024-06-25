from ping3 import ping
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(target):
    try:
        delay = ping(target)
        return delay is not None, target
    except Exception as e:
        print(f"Error pinging {target}: {e}")
        return False, target

def ping_all_hosts(hosts, domains, os_type):
    total_jobs = len(hosts) * len(domains)
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_fqdn = {}
        for domain in domains:
            print(f"Pinging hosts for {domain}")
            for r_host in hosts:
                fqdn = f"{r_host.strip()}.{domain}"
                future = executor.submit(ping_host, fqdn)
                future_to_fqdn[future] = fqdn

        completed_jobs = 0
        for future in as_completed(future_to_fqdn):
            completed_jobs += 1
            success, target = future.result()
            if target:
                results.append((success, target))
            print(f"Progress: {completed_jobs}/{total_jobs} jobs completed.")

        print("\nPingable hosts:")
        for success, target in results:
            if success:
                if os_type == "Linux":
                    print(f"\033[92m{target} is reachable.\033[0m")
                elif os_type == "Windows":
                    print(f"{target} is reachable.")

# Replace these with your actual hosts and domains
hosts = ["host1", "host2", "host3"]
domains = ["domain1", "domain2", "domain3"]
os_type = "Linux"  # or "Windows"

ping_all_hosts(hosts, domains, os_type)