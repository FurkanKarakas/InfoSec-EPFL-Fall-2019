import hashlib
import random
import binascii
import websockets
import asyncio
import sys
import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# parameters
N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3", 16)
g = 2
password = "PQAEDBQOAAAcBkUSVCgQHQcCDhcH"


def generaterandom(limit):
    ran = random.randrange(10**80)
    myhex = "%064x" % ran

    # limit string to [limit] characters
    myhex = myhex[:limit]
    return int(myhex, 16)


def encodeint(num):
    buff = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    return binascii.hexlify(buff).decode("utf-8")


def decodeint(numencoded):
    buff = binascii.unhexlify(numencoded)
    return int.from_bytes(buff, 'big')


async def hello():
    async with websockets.connect(
            'ws://com402.epfl.ch/hw2/ws') as websocket:

        # send email
        U = "serif.serbest@epfl.ch"
        Uencoded = U.encode("utf-8")
        await websocket.send(Uencoded)
        print("u encoded:", Uencoded)
        print("email sent")

        # receive salt
        saltencoded = await websocket.recv()
        salt = decodeint(saltencoded)
        print("salt encoded:", saltencoded)
        print("salt:", salt)

        # generate a random number
        a = generaterandom(32)

        # calculate and send A
        A = pow(g, a, N)
        Aencoded = encodeint(A)
        print("encoded A:", Aencoded)
        await websocket.send(Aencoded)

        # receive B
        Bencoded = await websocket.recv()
        B = decodeint(Bencoded)
        print("B encoded:", Bencoded)
        print("B:", B)

        # hash A and B
        Abytes = A.to_bytes((A.bit_length() + 7) // 8, 'big')
        Bbytes = B.to_bytes((B.bit_length() + 7) // 8, 'big')
        hashinput = Abytes + Bbytes
        u = hashlib.sha256(hashinput).hexdigest()
        print("u:", u)

        # hash salt, U and password
        passwordbytes = password.encode("utf-8")
        Ubytes = Uencoded
        hashinput = Ubytes + ":".encode("utf-8") + passwordbytes
        inputright = hashlib.sha256(hashinput).hexdigest()
        inputrightbytes = binascii.unhexlify(inputright)

        saltbytes = salt.to_bytes((salt.bit_length() + 7) // 8, 'big')
        hashinput = saltbytes + inputrightbytes

        x = hashlib.sha256(hashinput).hexdigest()
        print("x:", x)

        # calcuate S
        xint = int(x, 16)
        base = B - pow(g, xint, N)
        print("base:", base)

        uint = int(u, 16)
        exponent = a + uint * xint
        exponent = pow(exponent, 1, N)
        print("exponent:", exponent)

        S = pow(base, exponent, N)
        print("S:", S)

        # hash A, B and S
        Sbytes = S.to_bytes((S.bit_length() + 7) // 8, 'big')
        hashinput = Abytes + Bbytes + Sbytes
        response = x = hashlib.sha256(hashinput).hexdigest()

        # get token
        await websocket.send(response)
        Token = await websocket.recv()
        print("Token:", Token)


if __name__ == '__main__':
    try:
        print('connecting ...')
        asyncio.get_event_loop().run_until_complete(hello())

    except Exception as e:
        logging.exception(e)
