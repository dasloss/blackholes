from mongoengine import *
from hashlib import sha256

class User(Document):
    username = StringField(required=True)
    name = StringField(required=False)
    email = EmailField(required=False)
    password = BinaryField(required=False)
    active = BooleanField(default=True)
    service = StringField()
    authenticated = BooleanField(default=False)
    connected = BooleanField(default=False)
    def is_authenticated(self):
        return self.authenticated
    def set_password(self, password):
        self.password = "{SHA}" + sha256(password).digest()
    def check_password(self, password):
        return sha256(password).digest() == self.password[5:]
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username
    meta = {'allow_inheritance': True}

class Event(Document):
        name = StringField(required = True)
        startTime = DateTimeField(requried = True)
        endTime = DateTimeField(required = True)
        intervalMinutes = IntField()
        priority = IntField(default = 0)
        type = StringField()
        def get_name(self):
                return self.name
        meta = {'allow_inheritance': True}
