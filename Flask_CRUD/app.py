from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)
# connecting with Database
app.config["MONGO_URI"] = "mongodb://localhost:27017/address_book"
mongo_client = PyMongo(app)
db = mongo_client.db


class Crud(Resource):
    def get(self):
        data = list(db.users.find())
        for itr in data:
            itr["_id"] = str(itr["_id"])
        return jsonify(data)

    def post(self):
        result = {
            'Name': request.form['Name'],
            'PhoneNumber': request.form['PhoneNumber']
        }
        db.users.insert_one(result)
        return jsonify(message='Success')


class CrudName(Resource):
    def get(self, name):
        data = list(db.users.find({"Name":name}))
        for itr in data:
            result = {"Name": itr["Name"], "PhoneNumber": itr["PhoneNumber"]}
        return jsonify(result)

    def patch(self, name):
            db.users.update_one({"Name": name}, {"$set": {"PhoneNumber": request.form['PhoneNumber']}})
            return jsonify(message="User Updated")

    def delete(self, name):
            db.users.delete_one({"Name": name})
            return jsonify(message="Deleted")


api.add_resource(Crud, '/get')
api.add_resource(CrudName, '/get/<name>')


if __name__ == "__main__":
    app.run(debug=True, port=80)