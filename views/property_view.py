from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import PageofPartnershipSchema, PartnershipSchema
from model import Partnership
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class PartnershipView(FlaskView):
    route_base = '/property/'
    partnerships_schema = PageofPartnershipSchema()
    partnership_schema = PartnershipSchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_partnership = params.get('id_partnership', None)
        string = 'partnerships'

        partnership_data = Partnership.query
        if not id_partnership:
            partnerships_data = partnership_data.order_by(Partnership.name.asc()).paginate(int(page), int(per_page),
                                                                                           error_out=False)
            partnership = self.partnerships_schema.dump(partnerships_data).data
        else:
            partnerships_data = partnership_data.filter(Partnership.id == id_partnership).first()
            partnership = self.partnership_schema.dump(partnerships_data).data
            string = "partnership"

        return jsonify({string: partnership})

    def post(self):
        data = request.json
        partnership_obj = Partnership()

        partnership_obj.date_created = datetime.now()
        partnership_obj.name = data.get('name', None)
        if not partnership_obj.name:
            raise BadRequest('Name is Mandatory')
        partnership_obj.address = data.get('address', None)
        if not partnership_obj.address:
            raise BadRequest('Address is Mandatory')
        partnership_obj.id_neighborhood = data.get('id_neighborhood', None)
        if not partnership_obj.id_neighborhood:
            raise BadRequest('Id Neighborhood is Mandatory')
        admin_user = data.get('user', None)
        if not admin_user:
            raise BadRequest('Admin user is Mandatory')
        partnership_obj.id_user = admin_user.get('id_user', None)
        if not partnership_obj.id_user:
            raise BadRequest('Admin user is Mandatory')

        try:
            db.session.add(partnership_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store new partnership for user ')

        partnership = Partnership.query.order_by(Partnership.date_created.desc()).first()
        partnership_data = self.partnership_schema.dump(partnership).data

        return jsonify({'partnership': partnership_data})
