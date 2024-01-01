import socket
import re

ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
port_min = 0
port_max = 65535

open_ports = []

while True:
    ip_add_entered = input("\nEnter the Ip Address : ")
    if ip_add_pattern.search(ip_add_entered):
        print(f"\n{ip_add_entered} is valid")
        break

while True:
    port_range = input("""
    Range of ports you want to scan : <int>-<int>\n
    Enter port range : """)

    port_range_valid = port_range_pattern.search(port_range.replace(" ", " "))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

for port in range(port_min, port_max + 1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip_add_entered, port))
            open_ports.append(port)
    except:
        print(f"Could not connect to : {port}

print(f"Closed ports on {ip_add_entered} : ", int(port_max-port_min-1)-len(open_ports))
print(f"Open   ports on {ip_add_entered} : ", len(open_ports))
for outp in open_ports:
    print(outp)
