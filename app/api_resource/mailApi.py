# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask.ext.restful import Resource
from app.auth import auth
from app.models import User
from app import app
from app.mail import send_email
from itsdangerous import URLSafeTimedSerializer

def generate_validate_email(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def validate_token(token, expiration=3600): # email validate expiration 1 hours
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def sendmail(email):
    token = generate_validate_email(email)
    link = 'http://localhost:8888/api/v1/mail/'+token
    return send_email(email, 'jigsaw validate email', '<div><a href="'+link+'">'+link+'</a>链接有效时间为1小时</div>')

class SendAPI(Resource):
    #@auth.login_required
    def post(self):
        email = request.json.get('email')
        if email is None:
            return jsonify({'Success': 0})

        return jsonify({'Success': sendmail(email)})

class ValidAPI(Resource):
    def get(self, token):
        try:
            email = validate_token(token)
        except:
            return 'The confirmation link is invalid or has expired.', 200

        user = User.objects(email=email).first()
        if user is not None:
            if user.valid == 1:
                return 'Account already confirmed. Please login.', 200
            else:
                user.update(set__valid=1)
                return 'You have confirmed your account. Thanks!', 200
        return 'The confirmation link is invalid or has expired.', 200
