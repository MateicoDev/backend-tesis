from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import UserReducedSchema, PageOfUsersSchema
from model import User
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class UsersView(FlaskView):
    route_base = '/users/'
    users_schema = PageOfUsersSchema()
    user_schema = UserReducedSchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_user = params.get('id_user', None)
        string = 'users'

        user_data = User.query
        if not id_user:
            users_data = user_data.order_by(User.user_name.asc()).paginate(int(page), int(per_page), error_out=False)
            users = self.users_schema.dump(users_data).data
        else:
            user_data = user_data.filter(User.id == id_user).first()
            users = self.users_schema.dump(user_data).data
            string = "user"

        return jsonify({string: users})
