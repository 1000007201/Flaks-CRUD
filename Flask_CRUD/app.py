from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine
from models import Users


app = Flask(__name__)
api = Api(app)

# connecting with Database
app.config['MONGODB_SETTINGS'] = {
    "db": "address_book",
}

db = MongoEngine(app)


class Crud(Resource):
    def get(self):
        data = Users.objects()
        data_ = []
        for itr in data:
            data_.append({"Name": itr["Name"], "PhoneNumber": itr["PhoneNumber"]})
        return jsonify(data_)

    def post(self):
        data = Users(Name=request.form['Name'], PhoneNumber=request.form['PhoneNumber'])
        data.save()
        return jsonify(message='Success')


class CrudName(Resource):
    def get(self, name):
        data = Users.objects(Name=name).first()
        result = {"Name": data.Name, "PhoneNumber": data.PhoneNumber}
        return jsonify(result)

    def patch(self, name):
        data = Users.objects(Name=name).first()
        data.update(Name=name, PhoneNumber=request.form["PhoneNumber"])
        return jsonify(message="User Updated")

    def delete(self, name):
            data = Users.objects(Name=name).first()
            data.delete()
            return jsonify(message="Deleted")


api.add_resource(Crud, '/get')
api.add_resource(CrudName, '/get/<name>')


if __name__ == "__main__":
    app.run(debug=True, port=80)