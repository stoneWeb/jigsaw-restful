from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import datetime

cfg = app.config
#print app.config['SECRET_KEY']

class User(db.Document):
    uid = db.IntField(default=0)
    name = db.StringField()
    email = db.StringField(required=True)
    valid = db.IntField(default=0, min_value=0, max_value=1)
    time = db.DateTimeField(default = datetime.datetime.now())
    password = db.StringField(required=True)
    question = db.ListField(default=[])
    pushId = db.StringField()
    # other = {age: '', occupation, education, location, origin, mobOs, pcOs, gender, job, mobBrand}
    other = db.StringField(default='')

    def saveNewsUser(self):
        Ids_all.objects.first().update(inc__userId=1)
        self.uid = Ids_all.objects.first().userId
        self.password = self.hash_psw(self.password)
        self.save()
        return self

    def hash_psw(self, psw):
        return pwd_context.encrypt(psw)

    def verify_password(self, psw):
        return pwd_context.verify(psw, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(cfg['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'uid': self.uid})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(cfg['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.objects(uid=data['uid']).first()
        return user

class Ids_all(db.Document):
    userId = db.IntField(default=0)
    questionId = db.IntField(default=0)
    taskId = db.IntField(default=0)


class Questionnaire(db.Document):
    sid = db.IntField(default=0)
    title = db.StringField(required=True)
    question = db.StringField(required=True)
    description = db.StringField()
    time = db.DateTimeField(default=datetime.datetime.now())

    def saveNews(self):
        Ids_all.objects.first().update(inc__questionId=1)
        self.sid = Ids_all.objects.first().questionId
        self.save()
        return self

class Task(db.Document):
    sid = db.IntField(default=0)
    title = db.StringField(required=True)
    users = db.ListField()
    question = db.IntField(required=True)
    duration = db.DateTimeField()
    reminder = db.StringField()
    time = db.DateTimeField(default=datetime.datetime.now())

    def saveNews(self):
        Ids_all.objects.first().update(inc__taskId=1)
        self.sid = Ids_all.objects.first().taskId
        self.save()
        return self

class Result(db.Document):
    taskId = db.IntField(required=True)
    result = db.StringField()

if Ids_all.objects.first() is None:
    Ids_all().save()
