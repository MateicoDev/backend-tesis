from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import UserReducedSchema, PartnershipSchema, PropertySchema
from model import User
from model import Property, Partnership
from model import PropertyPerUser
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests


class LoginView(FlaskView):
    route_base = '/login'
    user_schema = UserReducedSchema()
    property_schema = PropertySchema()
    partnership_schema = PartnershipSchema()

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

        propertiesPerUser = PropertyPerUser.query.filter(PropertyPerUser.id_user == user.id).all()
        propiedades = []

        for item in propertiesPerUser:
            propiedad = Property.query.filter(Property.id == item.id_property).first()
            propiedad_data = self.property_schema.dump(propiedad, many=False).data
            consorcio = Partnership.query.filter(Partnership.id == propiedad.partnership.id)
            consorcio_data = self.partnership_schema.dump(consorcio, many=False).data
            propiedades.append([propiedad_data, consorcio_data])

        #consorcios = []

        #for item in propiedades:
        #    consorcio = Partnership.query.filter(Partnership.id == item.id_partnership)
        #    consorcios.append(consorcio)



        return jsonify({'user': user_data, 'propiedades': propiedades})

    #DEBO BUSCAR POR LA PROPIEDAD DEL USUARIO, EL ID DEL PARTNERSHIP A DONDE PERTENECE



    # @route('/social', methods=['POST'])
    # def post(self):
    #     try:
    #         idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    #         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
    #             raise ValueError('Wrong issuer.')
    #         userid = idinfo['sub']
    #     except ValueError:
    #         raise Forbidden('User not found')



