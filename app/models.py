from mongoengine import *
from hashlib import sha256

class User(Document):
    username = StringField(required=True, unique=True)
    #name = StringField(required=True)
    email = EmailField(required=False)
    password = BinaryField(required=False)
    #site = URLField()
    authenticated = BooleanField(default=False)
    active = BooleanField(default=True)
    oauth_token = StringField()
    oauth_secret = StringField()
    service = StringField()
    def set_password(self, password):
        self.password = "{SHA}" + sha256(password).digest()
    def check_password(self, password):
        return sha256(password).digest() == self.password[5:]
    def is_authenticated(self):
        return self.authenticated
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username
