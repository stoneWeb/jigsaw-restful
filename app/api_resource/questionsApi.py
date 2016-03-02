# -*- coding: utf-8 -*-

from flask import abort, jsonify, request, g
from flask.ext.restful import Resource
from app.auth import auth
from app.models import Questionnaire
import base64, json, re


def filterQuesModel(Q):
    other = getOtherFiled(Q.question) or ''
    _ret = {
        'sid': Q.sid,
        'title': Q.title,
        'description': Q.description,
        'question': other,
        'time': Q.time
    }
    return _ret

def getOtherFiled(fstr):
    if fstr == '':
        fstr = base64.encodestring('{}')
    try:
        fstr = json.loads(base64.decodestring(fstr))
    except:
        return False
    return fstr

class QuestionsAPI(Resource):
    def get(self):
        _ref = map(filterQuesModel, Questionnaire.objects.all())
        return jsonify({'Success': 1, 'data': _ref})

    def post(self):
        data = request.json
        if data is None or data.get('title') is None \
            or data.get('description') is None \
            or data.get('question') is None:
            return jsonify({'Success': 0})

        title = data.get('title').strip()
        description = (data.get('description') or '').strip()
        q = data.get('question')
        q = base64.encodestring(json.dumps(q))

        question = Questionnaire(title=title, description=description, question=q)
        question.saveNews()
        return jsonify({'Success': 1, 'id': question.sid})

class QuestionAPI(Resource):
    def get(self, sid):
        question = Questionnaire.objects(sid=sid).first()
        if not question:
            return jsonify({'Success': 0, 'message': 'Not Question!'})
        return jsonify({'Success': 1, 'data': filterQuesModel(question)})

    def put(self, sid):
        req = request.json
        ques = Questionnaire.objects(sid=sid).first()
        if ques is None or req is None:
            return jsonify({'Success': 0})

        fds = ['title', 'description', 'question']
        _ref = {}
        for key in fds:
            if req.get(key) is not None:
                if key == 'question':
                    _ref[key] = base64.encodestring(json.dumps(req.get(key)))
                else:
                    _ref[key] = req.get(key)

        _ref = dict(("set__%s" % k, v) for k,v in _ref.iteritems())
        ques.update(**_ref)
        return jsonify({'Success': 1})

    def delete(self, sid):
        if g.get('user') is None or g.user.uid > 1:
            return jsonify({'Success': 0, 'message': 'No Access!'})
        return jsonify({'Success': Questionnaire.objects(sid=sid).delete()})
