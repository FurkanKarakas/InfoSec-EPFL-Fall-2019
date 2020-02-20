from netfilterqueue import NetfilterQueue
from scapy.all import *
import re

def print_and_accept(packet):
    pkt = IP(packet.get_payload())
    if pkt.haslayer(Raw):
        # print(pkt.load)
        if pkt.load.find(b'\x00\x35') == -1:
            pass
        else:
            pkt.load.replace(b'\x00\x35', b'\x00\x2f')
            packet.set_payload(pkt.load)
            print('Sending replaced packet...')
    packet.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
