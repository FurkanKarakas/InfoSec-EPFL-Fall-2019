import base64
import hashlib
import hmac
import time
#from flask import Flask, request, make_response, abort
import flask
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = flask.Flask(__name__)


key = "PQAEDBQOAAAcBkUSVCgQHQcCDhcH"
cookie_name = 'LoginCokie'


def create_sha256_signature(key, message):
    byte_key = key.encode("utf-8")
    message = message.encode("utf-8")
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    # get user and password
    data = flask.request.get_json()
    username = data["username"]
    userpassword = data["password"]
    timestamp = int(time.time())
    print("username:", username, "userpwd:", userpassword,
          "timestamp:", timestamp, file=sys.stderr)

    # initialize cookie
    cookie = ""
    if username == "admin" and userpassword == "42":
        print("Admin identified", file=sys.stderr)
        cookie = username + "," + \
            str(timestamp) + ",com402,hw2,ex3,admin"
    else:
        print("User is not administrator", file=sys.stderr)
        cookie = username + "," + str(timestamp) + ",com402,hw2,ex3,user"

    HMAC = create_sha256_signature(key, cookie)
    cookie = cookie + "," + HMAC
    print("HMAC:", HMAC, file=sys.stderr)
    print("Cookie:", cookie, file=sys.stderr)

    # send cookie
    print("sending cookie", file=sys.stderr)
    cookie64 = base64.b64encode(cookie.encode('utf-8'))
    response = flask.Response
    response.set_cookie(cookie_name, cookie64)
    return response, 200


@app.route('/auth', methods=['GET'])
def auth():
    # decode cookie
    cookie64received = flask.request.cookies.get(cookie_name)
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
    flask.abort(403)


if __name__ == '__main__':
    app.run()
