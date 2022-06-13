import requests
import time

class Device:
    def __init__(self, mac, ip=None, name=None):
        self.mac = mac
        self.ip = ip
        self.name =  name

    def get_ip(self):
        return self.ip

    def get_mac(self):
        return self.mac

    def get_name(self):
        return self.name

    def get_company(self): 
        f = open('macscomp.txt', 'r')
        lines = f.readlines()
        
        mac = self.mac[:8].replace(":", "")
        for line in lines:
            vals = line.split(" ", 1)
            if vals[0] == mac:
                return vals[1][:-1]
        return "unknown"
    
    def get_list(self):
        return [self.mac, self.ip, self.name, self.get_company()]
    
    def __str__(self):
        return " MAC: " + self.mac + " IP: " + str(self.ip) + " Name: " + str(self.ip) + " Company: " + self.get_company()
