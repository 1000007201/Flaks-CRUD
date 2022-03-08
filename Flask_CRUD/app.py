from flask import Flask, jsonify, request
from flask_pymongo import PyMongo


app = Flask(__name__)

# connecting with Database
app.config["MONGO_URI"] = "mongodb://localhost:27017/address_book"
mongo_client = PyMongo(app)
db = mongo_client.db


@app.route('/add', methods=['POST'])
def add_value():
    result = {
        'Name': request.form['Name'],
        'PhoneNumber': request.form['PhoneNumber']
    }
    db.users.insert_one(result)
    return jsonify(message='Success')


@app.route('/get/allUsers', methods=['GET'])
def get_users():
    data = list(db.users.find())
    for itr in data:
        itr["_id"] = str(itr["_id"])
    return jsonify(data)


@app.route('/get/<name>', methods=['GET'])
def get_name(name):
    data = list(db.users.find({'Name':name}))
    for itr in data:
        result = { "Name": itr["Name"], "PhoneNumber": itr["PhoneNumber"]}

    return jsonify(result)


@app.route('/update/<name>', methods=['PATCH'])
def update(name):
    db.users.update_one({"Name":name}, {"$set":{"PhoneNumber":request.form['PhoneNumber']}})
    return jsonify(message="User Updated")


@app.route('/delete/<name>', methods=['DELETE'])
def delete(name):
    db.users.delete_one({"Name":name})
    return jsonify(message="Deleted")


if __name__ == "__main__":
    app.run(debug=True, port=80)