from mongoengine import *
from hashlib import sha256
# from pymongo import Connection

class User(Document):
    username = StringField(required=True)
    name = StringField(required=False)
    email = EmailField(required=False)
    password = BinaryField(required=False)
    active = BooleanField(default=True)
    service = StringField()
    oauth_token = StringField()
    oauth_secret = StringField()
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

class Candidate(Document):
    candidatename = StringField(required=True)
    electedoffice = StringField(required=True)
    maxdonation = IntField(required=True)
    bio = StringField(required=True)
    website = URLField(required=True, verify_exists=True)
    paymentkey = StringField(required=True)
    imgpath = StringField(required=False)

''' pymongo approach to db manipulation
_CONN = None
def get_mongo_connection():
    global _CONN
    if _CONN is None:
        if environment == "local":
            _CONN = Connection(host=DB_HOST, port=DB_PORT)
        elif environment == "cloud":
            _CONN = Connection(MONGO_URI)
    return _CONN

def get_db():
    return get_mongo_connection()[DB]

def query_candidates():
    db = get_db()
    for candidate in db.candidates.find({}):
        candidate = Candidate(**candidate)
        yield candidate

def insert_candidate(candidate):
    db = get_db()
    db.candidates.insert(vars(thing))

def clear_candidates():
    db = get_db()
    db.candidates.remove()
'''
