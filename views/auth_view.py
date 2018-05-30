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

        user_data = User.query
        if user_email:
            user = user_data.filter(User.email == user_email).first_or_404()
        else:
            raise Forbidden('User email its mandatory')

        user_data = self.user_schema.dump(user, many=False).data

        return jsonify({'user': user_data})
