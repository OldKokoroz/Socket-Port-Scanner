import re
import os
import socket
import subprocess
from time import localtime, strftime


ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

open_ports = []
closed_ports = []
out_time = 1  # default value

# -------------------
open_ports.clear()
closed_ports.clear()
# -------------------

print("=" * 75)

while True:
    at_first = input("""
Do you know the IP ?
    1 - Yes
    2 - No; Ping the domain
    
|-> """)

    if at_first == "2":
        dom = input("\nDomain: ")
        check = subprocess.run(f"ping -c 5 {dom}", shell=True, capture_output=True, text=True)

        print("\n" + check.stdout)

    ip_add_entered = input("""\nEnter the Ip Address: """)
    if ip_add_pattern.search(ip_add_entered):
        print(f"\n{ip_add_entered} is valid")
        break

while True:
    port_range = input("""
    Range of ports you want to scan: 1-1000\n
    Enter port range: """)

    scan_type = input("""
Scan Type:
    1 - Fast [Default]
    2 - Mid   
    3 - Detailed
    
|-> """)

    if scan_type == "1":
        out_time = 1
    elif scan_type == "2":
        out_time = 5
    elif scan_type == "3":
        out_time = 10

    port_range_valid = port_range.strip().split("-")

    if port_range_valid:
        port_min = int(port_range_valid[0])
        port_max = int(port_range_valid[1])

        port_list = range(port_min, port_max + 1)
        break


def sock_con(ip, port_1, timee):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timee)
        s.connect((ip, port_1))


for port in port_list:
    try:
        sock_con(ip_add_entered, port, out_time)
        open_ports.append(str(port))

    except KeyboardInterrupt:
        print("\nExiting Program !!!!")
        exit(0)
    except socket.gaierror:
        print("\nHostname Could Not Be Resolved !!!!")
        exit(1)
    except socket.error:
        closed_ports.append(str(port))


with open(f"{ip_add_entered}.txt", "a") as log:

    log.writelines(f"""\n\n\n{strftime("%d.%m.%Y - %H:%M:%S", localtime())}{" " * 51}{os.getuid()}\n{"=" * 75}
{len(open_ports)}   Open ports on {ip_add_entered} : 
    {open_ports}
\n\n
{len(closed_ports)}  Closed ports on {ip_add_entered} : 
    {closed_ports}
{"=" * 75}
""")

print("=" * 75)
