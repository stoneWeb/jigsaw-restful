# -*- coding: utf-8 -*-

from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import URLSafeTimedSerializer
from flask import g
from app.models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, psw):
    # verify email or token
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.objects(email=email_or_token).first()
        if not user or not user.verify_password(psw):
            return False
    g.user = user
    return True
