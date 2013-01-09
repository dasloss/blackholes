from mongoengine import *
from hashlib import sha256
import settings

class User(Document):
    username = StringField(required=True)
    name = StringField(required=False)
    email = EmailField(required=False)
    password = BinaryField(required=False)
    active = BooleanField(default=True)
    service = StringField()
    stripe_customer_id = StringField(required=False)
    authenticated = BooleanField(default=False)
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
    def set_stripe_customer_id(self, stripe_customer_id):
        self.stripe_customer_id = stripe_customer_id
    meta = {'allow_inheritance': True}
    # Special user fields who get money from other users
    special = BooleanField(default=False)
    special_name = StringField(required=False)
    special_info = StringField(required=False)
    special_website = URLField(required=False, verify_exists=True)
    special_info = StringField(required=False)
    token = StringField(required=False)                            
    connected = BooleanField(default=False)
    special_img = StringField(required=False)
    def set_token(self, token):
        self.token = token
    def is_connected(self):
        return self.connected
    def is_special(self):
        return self.special
