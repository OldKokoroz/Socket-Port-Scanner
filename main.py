import re
import socket
import subprocess
from time import localtime, strftime
from database import ports_dict, banner


class Deus:
    def __init__(self,
                ip_add_pattern = re.compile("^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$"),
                port_range_pattern = re.compile("([0-9]+)-([0-9]+)"),
                ip_add_entered = "",
                port_min = 1,
                port_max = 65535,
                out_time = 1,
                open_ports = "\n",
                counter1 = 0,
                counter2 = 0) -> None:
    
        self.port_min = port_min
        self.port_max = port_max
        self.out_time = out_time
        self.counter1 = counter1  # for open ports
        self.counter2 = counter2  # for closed ports
        self.open_ports = open_ports
        self.ip_add_pattern = ip_add_pattern
        self.ip_add_entered = ip_add_entered
        self.port_range_pattern = port_range_pattern
        

    def catch_dom(self) -> None:
        try:
            dom = input("""
1 - Domain 
2 - Host Name

|-> """)
        
            if dom == "1":
                domain = input("\nDomain: ")

                check = subprocess.run(f"ping -c 3 {domain}", shell=True, capture_output=True, text=True)
                print(f"\n {check.stdout}")
            
            if dom == "2":
                hostname = input("""\n
===== Device Must Be On The Same Network =====
Hostname: """)
                
                check1 = subprocess.run(f"nslookup {hostname}", shell=True, capture_output=True, text=True)
                arp = subprocess.run(f"arp -a", shell=True, capture_output=True, text=True)
                print("Couldn't find it? These are the devices on your network:")

                print(f"\n{check1.stdout}")
                print(f"\n{arp.stdout}")


        except KeyboardInterrupt:
            print("\nQuitting!")
            exit(0)

    def sock_search(self) -> None:
        try:
            self.ip_add_entered = input("""\nEnter the Ip Address: """)
            if self.ip_add_pattern.search(self.ip_add_entered):
                print(f"\n{self.ip_add_entered} ✅")

        except KeyboardInterrupt:
            print("\nQuitting!")
            exit(0)

    def sock_con(self, ip, port1, timee) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timee)
                s.connect((ip, port1))

        except KeyboardInterrupt:
            print("\nQuitting!")
            exit(0)

    def con_loop(self) -> None:
        self.port_range_valid = self.port_range.strip().split("-")

        if self.port_range_valid:
            self.port_min = int(self.port_range_valid[0])
            self.port_max = int(self.port_range_valid[1])

            self.port_list = range(self.port_min, self.port_max + 1)

        for port in self.port_list:
            try:
                self.sock_con(self.ip_add_entered, port, self.out_time)
                self.open_ports += f"\t\t{port}\t\t: {ports_dict[port]}\n"
                self.counter1 += 1

            except KeyboardInterrupt:
                print("\nExiting Program !!!!")
                exit(0)

            except socket.gaierror:
                print("\nHostname Could Not Be Resolved !!!!")
                exit(1)

            except socket.error:
                self.counter2 += 1
    

    def saver(self) -> None:
        message = f"""\n\n\n{strftime("%d.%m.%Y - %H:%M:%S", localtime())}{" " * 34} Port Range: {self.port_min}-{self.port_max}\n{"=" * 75}
{self.counter2}   Ports are closed on {self.ip_add_entered}\n
{self.counter1}   Open ports on {self.ip_add_entered} :
{self.open_ports}
{"=" * 75}\n"""
        
        with open(f"{self.ip_add_entered}.txt", "a") as log:
            log.writelines(message)
    

    def starter(self):
        print("=" * 75)
        print(banner)
        while True:
            at_first = input("""
Do you know the IP ?
    1 - Yes
    2 - No, Ping the domain

|-> """)
            
            if at_first == "1":
                self.sock_search()
                break

            elif at_first == "2":
                self.catch_dom()
                self.sock_search()
                break

            else:
                print("\nInvalid Choice ❌")

        while True:
            self.port_range = input("""\n
Range of ports you want to scan: 1-1000\n
Enter port range: """)

            self.scan_type = input("""
Scan Type:
    1 - Fast 〥
    2 - Mid  
    3 - Detailed

|-> """)

            if self.scan_type == "1":
                self.out_time = 1
                break
            elif self.scan_type == "2":
                self.out_time = 5
                break
            elif self.scan_type == "3":
                self.out_time = 10
                break

            else:
                print("\nInvalid Choice ❌")

        self.con_loop()
        self.saver()
        print("=" * 75)


socket_ = Deus()
socket_.starter()
