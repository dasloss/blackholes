from mongoengine import *
from hashlib import sha256

class User(Document):
    username = StringField(required=True)
    name = StringField(required=True)
    email = EmailField(required=True)
    password = BinaryField(required=True)
    site = URLField()
    def check_password(self, password):
        return sha256(password).digest() == self.password[5:]
    def set_password(self, password):
        self.password = "{SHA}" + sha256(password).digest()
