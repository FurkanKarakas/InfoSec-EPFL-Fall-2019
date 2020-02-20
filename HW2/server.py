from flask import Flask, request, make_response, abort
from random import randint
import hmac
import hashlib
import base64
import sys
import time

app = Flask(__name__)
cookie_name = "LoginCookie"
key = "This is a random text, bro."


def create_sha256_signature(key, message):
    byte_key = key.encode("utf-8")
    message = message.encode("utf-8")
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/login", methods=['POST'])
def login():
    # get user data
    data = request.data
    print(data)
    username = request.form.get('username')
    password = request.form.get('password')
    timestamp = int(time.time())
    print('username:', username, 'password:', password,
          'timestamp:', timestamp, file=sys.stderr)
    # initialize cookie
    cookie = ''
    if username == 'admin' and password == '42':
        print('Admin identified', file=sys.stderr)
        cookie = username+','+str(timestamp)+',com402,hw2,ex3,admin'
    else:
        print('User is not admin', file=sys.stderr)
        cookie = username+','+str(timestamp)+',com402,hw2,ex3,user'

    HMAC = create_sha256_signature(key, cookie)
    cookie += ','+HMAC
    print("HMAC:", HMAC, file=sys.stderr)
    print("Cookie:", cookie, file=sys.stderr)

    # send cookie
    print("sending cookie", file=sys.stderr)
    cookie64 = base64.b64encode(cookie.encode('utf-8'))
    response = make_response()
    response.set_cookie("LoginCookie", cookie64)
    return response, 200


@app.route("/auth", methods=['GET'])
def auth():
    # decode cookie
    cookie64received = request.cookies.get('LoginCookie')
    print("This is my cookie", cookie64received)
    cookiereceived = base64.b64decode(cookie64received).decode('utf-8')
    print("Received cookie:", cookiereceived, file=sys.stderr)

    # extract received HMAC
    cookielist = cookiereceived.split(',')
    HMACreceived = cookielist.pop()
    print("Received HMAC:", HMACreceived, file=sys.stderr)

    # calculte expected HMAC
    cookie = ','.join(cookielist)
    HMACexpected = create_sha256_signature(key, cookie)
    print("Expected HMAC:", HMACexpected, file=sys.stderr)

    # validate cookie
    if HMACexpected == HMACreceived:
        username = cookielist[0]
        if username == "admin":
            return "Admin", 200
        else:
            return "User", 201
    abort(403)


if __name__ == '__main__':
    app.run()
