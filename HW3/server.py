from flask import Flask, request, make_response, abort
import bcrypt

app = Flask(__name__)


@app.route('/', methods=['POST'])
def get_user_data():
    # get user data
    data = request.get_json()
    user = data["user"]
    passwd = data["pass"]
    passwd_encoded = passwd.encode("utf-8")
    passwd_hash = bcrypt.hashpw(passwd_encoded, bcrypt.gensalt())
    return passwd_hash, 200


if __name__ == '__main__':
    app.run()
