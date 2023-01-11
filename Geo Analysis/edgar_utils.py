import re
import time
import pandas as pd
from flask import Flask, request
import netaddr
from bisect import bisect
ips = pd.read_csv("ip2location.csv")


def lookup_region(ip):
    #remove letters from IP replace with 0
    raw_IP = re.sub("[a-zA-Z]", "0", ip)
   
    #convert to integer
    int_IP = int(netaddr.IPAddress(raw_IP))
   
    #lookup with bisect for index#
    row_idx = bisect(ips['low'], int_IP) -1
    
    #return the region
    return ips.iloc[row_idx]['region']
    
class Filing:
    def __init__(self, html):
        self.addresses = self.getaddress(html) #self.findaddresses(html)
        self.dates = [x[0] for x in re.findall(r"((19|20)\d{2}-\d{2}-\d{2})", html)]
        self.sic = self.getSIC(html)
    
    def getSIC(self, html):
        SIC = re.findall(r"SIC.?(\d{3,4})", html)
        if len(SIC) == 0:
            return None
        return int(SIC[0])
    
    def getaddress(self, html):
        addr = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            addr1 = []
            for line in re.findall(r"mailerAddress\">([\s\S]+?)</span>", addr_html):
                addr1.append(line.strip())
            if len(addr1) > 0:
                addr.append("\n".join(addr1))
        condition = time.time()
        while("" in addr):
            addr.remove("")
            timeatm = time.time()
            if (timeatm - condition) > 1:
                break
            
        return addr
    
    def state(self):
        for x in self.addresses:
            abbreviate = re.search(r"([A-Z]{2}).?\d{5}", x)
            if abbreviate:
                return abbreviate.group(1)
        return None