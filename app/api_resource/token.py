# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.restful import Resource
from flask import g
from app.auth import auth

class GetAuthToken(Resource):
    decorators = [auth.login_required]
    def get(self):
        # 10 minute
        token = g.user.generate_auth_token(6000)
        return {'Success': 1, 'token': token.decode('ascii'), 'duration': 6000}
