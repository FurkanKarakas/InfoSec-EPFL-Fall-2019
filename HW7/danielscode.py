from bs4 import BeautifulSoup
from phe import paillier
import requests
import json


N = 2048
url = "http://0.0.0.0:8080/prediction"


public_key, private_key = paillier.generate_paillier_keypair(n_length=N)
secret_number_list = [0.48555949, 0.29289251, 0.63463107, 0.41933057,
                      0.78672205, 0.58910837, 0.00739207, 0.31390802, 0.37037496, 0.3375726]
encrypted_number_list = [public_key.encrypt(
    x, precision=2**(-16)).ciphertext() for x in secret_number_list]  # check this

response = requests.post(
    url, json={"pub_key_n": public_key.n, "enc_feature_vector": encrypted_number_list})
json_data = response.json()
ciphertext = json_data["enc_prediction"]
predNumberEncrypted = paillier.EncryptedNumber(
    public_key, ciphertext, exponent=-8)  # check this

print("predNumber=", private_key.decrypt(predNumberEncrypted))

# #
# assert 2**(-16) > abs(query_pred([0.48555949, 0.29289251, 0.63463107,
#                                   0.41933057, 0.78672205, 0.58910837,
#                                   0.00739207, 0.31390802, 0.37037496,
#                                   0.3375726 ]) -0.44812144746653826)
