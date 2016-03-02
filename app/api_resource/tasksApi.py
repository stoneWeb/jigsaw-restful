# -*- coding: utf-8 -*-

from flask import Flask
from flask import abort, jsonify, request, g
from flask.ext.restful import Resource
from app.auth import auth
from app.models import Task, User
import base64, json, re

def filterTaskModel(T):
    return {
        'sid': T.sid,
        'title': T.title,
        'question': T.question,
        'users': T.users,
        'duration': T.duration,
        'reminder': T.reminder,
        'time': T.time
    }

class TasksAPI(Resource):
    def get(self):
        _ref = map(filterTaskModel, Task.objects.all())
        return jsonify({'Success': 1, 'data': _ref})
    def post(self):
        data = request.json
        if data is None or data.get('title') is None \
            or data.get('users') is None \
            or data.get('question') is None:
            return jsonify({'Success': 0})

        title = data.get('title').strip()
        question = data.get('question')
        users = data.get('users') or []
        duration = data.get('duration')
        reminder = data.get('reminder')
        if len(users) < 1:
            return jsonify({'Success': 0})

        for key in users:
            u = User.objects(uid=key).first()
            if u is not None and question not in u.question:
                u.update(push__question=question)

        task = Task(title=title, question=question, users=users, duration=duration, reminder=reminder)
        task.saveNews()
        return jsonify({'Success': 1, 'id': task.sid})

class TaskAPI(Resource):
    def get(self, sid):
        task = Task.objects(sid=sid).first()
        if not task:
            return jsonify({'Success': 0, 'message': 'Not Task!'})
        return jsonify({'Success': 1, 'data': filterTaskModel(task)})
    def put(self):
        pass
    def delete(self):
        pass
