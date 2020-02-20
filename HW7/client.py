from phe import paillier
import requests
import json

precision = 2**-16


def query_pred(x):
    url = 'http://0.0.0.0:8080/prediction'
    public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)
    n = public_key.n
    # print(n, public_key.g, public_key.g == n+1, sep='\n')
    x_encrypted = [public_key.encrypt(
        element, precision=precision).ciphertext() for element in x]
    json_data = {'pub_key_n': n, 'enc_feature_vector': x_encrypted}
    response = requests.post(url, json=json_data)
    if response:
        enc_prediction = json.loads(response.content)['enc_prediction']
        predEncrypted = paillier.EncryptedNumber(
            public_key, enc_prediction, exponent=-8)  # The base is 16, and the precision doubles since we do a multiplication in the server and a single multiplication doubles the precision (from -16 to -32)
        prediction = private_key.decrypt(predEncrypted)

        return prediction
    else:
        print(response.text)


if __name__ == '__main__':
    assert 2**(-16) > abs(query_pred([0.48555949, 0.29289251, 0.63463107,
                                      0.41933057, 0.78672205, 0.58910837,
                                      0.00739207, 0.31390802, 0.37037496,
                                      0.3375726])-0.44812144746653826)

    parameters = [query_pred([0]*10)]
    for i in range(10):
        vector = [0]*10
        vector[i] = 1
        parameters.append(query_pred(vector)-parameters[0])

    print('Parameters:', parameters)
    actual_parameters = [0.05458201, 0.13526855, 0.02712842, 0.18588048, 0.0145351,
                         0.05692263, 0.10989505, 0.16611514, 0.04010465, 0.05390962, 0.15565836]
    print('Actual parameters:', actual_parameters)
    print('Are they equal?', parameters == actual_parameters)
