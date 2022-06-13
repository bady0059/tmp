from asyncio import threads
from socket import timeout
from device import Device
from router import Router
import threading
import socket
import scapy.all as scapy
from scapy.layers.dot11 import Dot11ProbeReq, Dot11, Dot11Beacon, RadioTap, Dot11Deauth, Dot11Elt
#from scapy.layers import TCP, IP
from scapy.layers.inet import IP, TCP
import scapy_p0f

class Scanner:

    def __init__(self, interface):
        self.interface = interface

    def __scan_devices_outside(self, pkt):
        if pkt.haslayer(Dot11):
            dot11_layer = pkt.getlayer(Dot11)
            macs = [dot11_layer.addr1, dot11_layer.addr2, dot11_layer.addr3]
            if dot11_layer.addr2 and "ff:ff:ff:ff:ff:ff" not in macs and "00:00:00:00:00:00" not in macs:
                if dot11_layer.addr2 not in self.__get_devices_mac() and dot11_layer.addr1 in self.__get_routers_mac():
                    print(self.router.get_mac(), dot11_layer.addr1)
                    if dot11_layer.addr1 == self.router.get_mac():
                        self.devices.append(Device(dot11_layer.addr2))
                        print(str(dot11_layer.addr2) + " is conected to " + str(dot11_layer.addr1) + " " + str(self.router.get_ssid()))



    def scan_devies_inside(self, router, list):
        ip = router.get_ip()+"/24"
        arp_packet = scapy.ARP(pdst=ip)
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_broadcast_packet = broadcast_packet / arp_packet
        answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
        devices = []
               
        for answer in answered_list:
            try:
                name = socket.gethostbyaddr(answer[1].psrc)[0]
                #---
                #self.get_os_of_devices(answer)
                #---
            except:
                name = "unknown"
            d = Device(answer[1].hwsrc, answer[1].psrc, name)
            devices.append(d)

            print(d.get_ip() + " " + d.get_mac() + " " + d.get_name() + " " + str(d.get_company()))
            
            list.append(d)

        return devices

    def get_os_of_devices(self, pkt):
        try:
            print(scapy_p0f.p0f(pkt))
        except Exception as e:
            print(e)

    def scan_open_ports(self, ip): #TODO: make it the best like nmap, ack
        def syn_ack(min_port, max_port):   
            for port in range(int(min_port), int(max_port)):
                respone = scapy.sr1(IP(dst=ip)/TCP(dport=port, flags="S"), verbose=False, timeout=.2)
                if respone:
                    if respone[TCP].flags == 18:
                        serviceName = socket.getservbyport(port, "tcp")
                        ports.append([port, serviceName])
                        print("Port " + str(port) + " is open " + serviceName)
                        

        ports = []
        num_of_threads = 10
        threads = []
        for i in range(num_of_threads):
            t = threading.Thread(target=syn_ack, args=(i*(1000/num_of_threads), (i+1)*(1000/num_of_threads)))
            t.daemon = True
            t.start()
            threads.append(t)
        
        for thread in threads:
            thread.join()

        print("done") 
        return ports



    def __scan_ap(self, pkt):
        if pkt.haslayer(Dot11):
            try:
                netName = pkt.getlayer(Dot11).info
                if netName.decode() not in self.__get_routers_names() and netName.decode() != "":
                    self.routers.append(Router(pkt.addr3, pkt.getlayer(Dot11).channel, netName))

            except:
                pass

        # hidden ssid
        if pkt.haslayer(Dot11Beacon):
            if not pkt.info and pkt.addr3 not in self.__get_routers_mac():
                self.routers.append(Router(pkt.addr3, pkt.getlayer(Dot11).channel, "Hidden SSID"))

    def __get_routers_names(self):
        ssids = []
        for router in self.routers:
            ssids.append(router.get_ssid())
        return ssids
    
    def __get_routers_mac(self):
        macs = []
        for router in self.routers:
            macs.append(router.get_mac())
        return macs
    
    def __get_devices_mac(self):
        macs = []
        for device in self.devices:
            macs.append(device.get_mac())
        return macs

    #---------------------
    def scan_routers(self, list):  
        self.interface.monitor_mode()
        t = threading.Thread(target=self.interface.channel_hop)
        t.daemon = True
        t.start()

        self.routers = []
        scapy.sniff(iface=self.interface.get_name(), prn=self.__scan_ap, store=0, timeout=14)
        self.interface.managed_mode()
        
        for r in self.routers:
            list.append(r)
            
        return self.routers

    def scan_devices_outside(self, router):
        self.interface.monitor_mode()
        self.interface.set_channel(router.get_channel())
        
        self.router = router

        self.devices = []
        scapy.sniff(iface=self.interface.get_name(), prn=self.__scan_devices_outside, store=0, timeout=3)
        self.interface.managed_mode()
        
        return self.devices
