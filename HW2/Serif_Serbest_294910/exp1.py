import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from flask import Flask, request, Response
import json
import base64
app = Flask(__name__)

def superencryption(msg):
    key = "Never send a human to do a machine's job"
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[0:diff]
    
    amsg = [ord(c) for c in msg]
    akey = [ord(c) for c in key[0: len(msg)]]
    
    s = ""
    for i in range(len(amsg)):
        b = amsg[i] ^ akey[i]
        s = s + chr(b)
    
    encoded = base64.b64encode(bytes(s, encoding='utf-8'))
    return encoded.decode("utf-8")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hw2/ex1', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        print('GET', file=sys.stderr)
    if request.method == 'POST':
        print('POST', file=sys.stderr)
        
        dic = request.get_json()
        print(dic, file=sys.stderr)
        
        user = dic['user']
        pwd = dic['pass']
        enc = superencryption(user)
        if enc == pwd:
            print('PASSWORD IS CORRECT', file=sys.stderr)
            response = Response(status=200)
        else:
            print('WRONG PASSWORD', file=sys.stderr)
            response = Response(status=400)
        
    return response
   

if __name__ == '__main__':
    try:
        app.run()
        print('testing', file=sys.stderr)

    except Exception as e: 
        logging.exception(e)
