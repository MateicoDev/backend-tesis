from flask_classy import FlaskView, route
from flask import jsonify, request

from schemas import PropertyPerUserSchema, RelationPropertyPerUserSchema
from schemas import PageOfPropertyPerUserSchema, PageOfRelationPropertyPerUser
from model import PropertyPerUser, RelationPropertyPerUser
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime

class PropertyPerUserView(FlaskView):
    route_base = '/propertyPerUser/'
    propertyPerUser_schema = PropertyPerUserSchema()
    propertiesPerUser_schema = PageOfPropertyPerUserSchema()
    relationPropertyPerUser_schema = RelationPropertyPerUserSchema()
    relationsPropertiesPerUser_schema = PageOfRelationPropertyPerUser()

    def post(self):
        data = request.json
        propertyperuser_obj = PropertyPerUser()

        propertyperuser_obj.date_created = datetime.now()

        user = data.get('id_user', None)
        if not user:
            raise BadRequest('Id user is Mandatory')
        propiedad = data.get('id_property', None)
        if not propiedad:
            raise BadRequest('Id property is Mandatory')
        relation = data.get('id_relation', None)

        propertyperuser_obj.id_user = user
        propertyperuser_obj.id_property = propiedad
        if not relation:
            propertyperuser_obj.id_relation = None
        else:
            propertyperuser_obj.id_relation = relation

        try:
            db.session.add(propertyperuser_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise  InternalServerError('Unable to store a new property per user')

        propertyperuser = PropertyPerUser.query.order_by(PropertyPerUser.date_created.desc()).first()
        propertyperuser_data = self.propertyPerUser_schema.dump(propertyperuser).data

        return jsonify({'Property Per User': propertyperuser_data})

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_user = params.get('id_user', None)

        propertyperuser = PropertyPerUser.query
        if not id_user:
            raise BadRequest('Id User is Mandatory')
        else:
            propertyperuser = propertyperuser.filter(PropertyPerUser.id_user == id_user).paginate(int(page),
                                                                                                  int(per_page),
                                                                                                  error_out=False)
            propertyperuser_data = self.propertiesPerUser_schema.dump(propertyperuser).data


        return jsonify({'Properties of User': propertyperuser_data})
