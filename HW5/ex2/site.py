#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw5_ex2"

# This method returns a list of messages in a json format such as
# [
# { "name": <name>, "message": <message> },
# { "name": <name>, "message": <message> },
# ...
# ]
# If this is a POST request and there is a parameter "name" given, then only
# messages of the given name should be returned.
# If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages", methods=["GET", "POST"])
def messages():
    with db.cursor() as cursor:

        sql = "SELECT name,message FROM messages "
        # display all messages
        if request.method == "GET":
            cursor.execute(sql)

        elif request.method == "POST":
            # get the POST search parameter
            name = request.form["name"]
            if name is not None:
                # Prepared statement. Use this to prevent SQL injections.
                sql += "WHERE name = %s"
                cursor.execute(sql, (name, ))
            else:
                return jsonify({'': ''}), 500
                # return 500
        #print("/message SQL: %s " % sql)
        # sys.stdout.flush()
        res = cursor.fetchall()
        # print(res)
        json = list()
        for i in range(len(res)):
            if {"name": res[i][0], "message": res[i][1]} not in json:
                json.append({"name": res[i][0], "message": res[i][1]})
        print(json)
        return jsonify(json), 200


# This method returns the list of users in a json format such as
# { "users": [ <user1>, <user2>, ... ] }
# This methods should limit the number of users if a GET URL parameter is given
# named limit. For example, /users?limit=4 should only return the first four
# users.
# If the paramer given is invalid, then the response code must be 500.
@app.route("/users", methods=["GET"])
def contact():
    with db.cursor() as cursor:
        # your code here
        limit = request.args.get('limit')
        if limit is not None:
            if limit.isdigit():
                limit = int(limit)
                sql = "SELECT name FROM users"
                cursor.execute(sql)
                res = cursor.fetchall()
                json = {"users": []}
                for i in range(int(limit)):
                    if res[i][0] not in json["users"]:
                        json["users"].append(res[i][0])
                return jsonify(json), 200
            else:
                return jsonify({'': ''}), 500
                # return 500
        elif limit is None:
            sql = "SELECT name FROM users"
            cursor.execute(sql)
            res = cursor.fetchall()
            json = {"users": []}
            for i in range(len(res)):
                if res[i][0] not in json["users"]:
                    json["users"].append(str(res[i][0]))
            return jsonify(json), 200


if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    # Here, db is a connection to a database. We store it in a variable.
    db = pymysql.connect("localhost",
                         username,
                         password,
                         database)
    with db.cursor() as cursor:
        populate.populate_db(seed, cursor)
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0', port=80)
