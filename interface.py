
import os
import netifaces
import time
import scapy.all as scapy

class Interface:
    def __init__(self, name):
        self.name = name
        self.mac = self.get_mac()

    def get_name(self):
        return self.name

    def get_mac(self):
        return netifaces.ifaddresses(self.name)[netifaces.AF_LINK][0]['addr']
    
    def get_ip(self):
        return netifaces.ifaddresses(self.name)[netifaces.AF_INET][0]['addr']

    def set_channel(self, num):
        os.system("iwconfig " + self.name + " channel " + str(num))

    def channel_hop(self, loops=2):
        for loop in range(loops):
            for c in range(1, 14):
                self.set_channel(int(c))
                time.sleep(1)

    def monitor_mode(self):
        os.system("ifconfig " + self.name + " down")
        os.system("iwconfig " + self.name + " mode monitor")
        os.system("ifconfig " + self.name + " up")
        time.sleep(1)

    def managed_mode(self):
        os.system("ifconfig " + self.name + " down")
        os.system("iwconfig " + self.name + " mode managed")
        os.system("ifconfig " + self.name + " up")
        time.sleep(1)

    def port_forwarding_on(self):
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    def port_forwarding_off(self):
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

    def send_packet(self, packet):
        scapy.send(packet, verbose=False, iface=self.name)
