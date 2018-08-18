from flask_classy import FlaskView
from flask import jsonify, request
from schemas import UserReducedSchema
from model import User
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class LoginView(FlaskView):
    route_base = '/login/'
    user_schema = UserReducedSchema()

    def post(self):
        data = request.json
        user_email = data.get('user_email', None)
        if not user_email:
            raise BadRequest('Email is mandatory')

        password = data.get('user_password', None)
        user = User.query.filter(User.email == user_email).first_or_404()
        if user is None:
            raise Forbidden('User not found')
        elif user.password != password:
            raise Forbidden('Password incorrect')

        user_data = self.user_schema.dump(user, many=False).data

        return jsonify({'user': user_data})
