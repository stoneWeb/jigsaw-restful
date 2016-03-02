# -*- coding: utf-8 -*-

from flask import abort, jsonify, request, url_for, g
from flask.ext.restful import Resource
from app.auth import auth
from app.models import User
from mailApi import sendmail
import base64, json, re

fields = ['age', 'occupation', 'education', 'location', 'origin', 'mobOs', 'pcOs', 'gender', 'job', 'mobBrand']
def filterUserModel(user):
    other = getOtherFiled(user.other)
    _ret = {
        'uid': user.uid,
        'email': user.email,
        'name': user.name,
        'valid': user.valid,
        'time': user.time
    }
    if other:
        _ret = dict(_ret, **other)
    return _ret

def getOtherFiled(fstr):
    if fstr == '':
        fstr = base64.encodestring('{}')

    try:
        fstr = json.loads(base64.decodestring(fstr))
    except:
        return False
    return fstr


class UsersAPI(Resource):
    def get(self):
        _ref = map(filterUserModel, User.objects.all())
        return jsonify({'Success': 1, 'data': _ref})
    def post(self):
        data = request.json or request.form
        if data is None:
            return jsonify({'Success': 0, 'message': 'No Data!'})

        email = data.get('email') or ''
        pwd   = (data.get('password') or '').strip()

        if re.match(r'^\w+@\w+?\.[a-zA-Z]{2,3}$', email) is None \
            or len(pwd) < 7 \
            or User.objects(email=email).first() is not None:
            return jsonify({'Success': 0, 'message': 'Invalid!'})

        _ref = {
            'email':email,
            'password': pwd,
            'name': data.get('name'),
            'pushId': data.get('pushId')
        }
        if g.get('user') is not None and g.user.uid == 1 and data.get('valid') is not None:
            _ref['valid'] = 1

        other = {}
        for key in fields:
            if data.get(key) is not None:
                other[key] = data.get(key)

        if len(other) > 0:
            _ref['other'] = base64.encodestring(json.dumps(other))
        _ref = dict(("%s" % k, v) for k,v in _ref.iteritems())
        user = User(**_ref)
        # password to hash
        user.saveNewsUser()
        if _ref.get('valid') is None:
            sendmail(email)
        return jsonify({'email': user.email}), 200, {'Location': url_for('get_user', uid = user.uid, _external = True)}

class UserAPI(Resource):
    def get(self, uid):
        user = User.objects(uid=uid).first()
        if not user:
            return jsonify({'Success': 0, 'message': 'Not User!'})
        return jsonify({'Success': 1, 'data': filterUserModel(user)})

    @auth.login_required
    def put(self, uid):
        data = request.json or request.form

        if g.get('user') is not None and data is not None:
            if uid != g.user.uid and g.user.uid != 1:
                return jsonify({'Success': 0, 'message': 'No Access!'})
        else:
            return jsonify({'Success': 0})

        user = User.objects(uid=uid).first()
        if not user:
            return jsonify({'Success': 0, 'message': 'Not User!'})

        _ref = {}
        # change password
        pwd = data.get('password')
        oldpwd = data.get('oldpassword')
        if pwd is not None:
            pwd = pwd.strip()
            if len(pwd) >= 7:
                if oldpwd is not None and user.verify_password(oldpwd):
                    pwd = user.hash_psw(pwd)
                    _ref['password'] = pwd
                else:
                    return jsonify({'Success': 0, 'message': 'old password error!'})
            else:
                return jsonify({'Success': 0, 'message': 'password invalid format!'})

        # filter safe fields
        other = getOtherFiled(user.other)
        fds = ['name','pushId']
        fds.extend(fields)

        for key in fds:
            if data.get(key) is not None:
                if key == 'name' or key == 'pushId':
                    _ref[key] = data.get(key)
                elif other is not False:
                    other[key] = data.get(key)

        if other:
            _ref['other'] = base64.encodestring(json.dumps(other))

        _ref = dict(("set__%s" % k, v) for k,v in _ref.iteritems())

        if len(_ref) == 0:
            return jsonify({'Success': 0})

        user.update(**_ref)
        return jsonify({'Success': 1})

    def delete(self, uid):
        if g.get('user') is None or uid == 1 or g.user.uid > 1:
            return jsonify({'Success': 0, 'message': 'No Access!'})

        return jsonify({'Success': User.objects(uid=uid).delete()})
