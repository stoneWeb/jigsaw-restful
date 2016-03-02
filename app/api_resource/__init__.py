# -*- coding: utf-8 -*-

from app import app
from flask.ext.restful import Api, Resource
api = Api(app)



import usersApi
import questionsApi
import tasksApi
import token

api.add_resource(usersApi.UsersAPI, '/api/v1/users', endpoint='users')
api.add_resource(usersApi.UserAPI, '/api/v1/users/<int:uid>', endpoint='user')
api.add_resource(questionsApi.QuestionsAPI, '/api/v1/questions', endpoint='questions')
api.add_resource(questionsApi.QuestionAPI, '/api/v1/questions/<int:sid>', endpoint='question')
api.add_resource(tasksApi.TasksAPI, '/api/v1/tasks', endpoint='tasks')
api.add_resource(tasksApi.TaskAPI, '/api/v1/tasks/<int:sid>', endpoint='task')
api.add_resource(token.GetAuthToken, '/api/v1/token', endpoint='token')
api.add_resource(mailApi.SendAPI, '/api/v1/mail', endpoint='mail_send')
api.add_resource(mailApi.ValidAPI, '/api/v1/mail/<token>', endpoint='mail_validate')
