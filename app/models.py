from mongoengine import *
from hashlib import sha256
from pymongo import Connection
import settings

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

_CONN = None
def get_mongo_connection():
    global _CONN
    if _CONN is None:
        if settings.environment == "local":
            _CONN = Connection(host=settings.DB_HOST, port=settings.DB_PORT)
        elif settings.environment == "cloud":
            _CONN = Connection(settings.MONGO_URI)
    return _CONN

def get_db():
    return get_mongo_connection()[settings.DB]

def query_candidates():
    db = get_db()
    for candidate in db.candidate.find({}):
        candidate = Candidate(**candidate)
        yield candidate

def insert_candidates(candidate):
    db = get_db()
    db.candidate.insert(vars(thing))

def clear_candidates():
    db = get_db()
    db.candidate.remove()
