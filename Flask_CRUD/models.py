import mongoengine as me


class Users(me.Document):
    Name = me.StringField(max_length=50, required=True)
    PhoneNumber = me.StringField(max_length=10, required=True)


