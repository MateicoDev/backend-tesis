from flask_classy import FlaskView, route
from flask import jsonify, request

# from model.property_model import Neighborhoods, Partnership
from schemas import PageOfPartnershipSchema, PartnershipSchema, PageOfNeighborhoodSchema, NeighborhoodSchema
from model import Partnership, Neighborhoods
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class PartnershipView(FlaskView):
    route_base = '/property/'
    partnerships_schema = PageOfPartnershipSchema()
    partnership_schema = PartnershipSchema()
    neighborhoods_schema = PageOfNeighborhoodSchema()
    neighborhood_schema = NeighborhoodSchema()

    @route('/partnership', methods=['GET'])
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

    @route('/partnership', methods=['POST'])
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

    @route('/partnership', methods=['PUT'])
    def put_partnership(self):
        data = request.json
        partnership_modify = Partnership()
        partnership_modify.id = data.get('id', None)
        partnership_modify.name = data.get('name', None)
        partnership_modify.address = data.get('address', None)
        partnership_modify.id_neighborhood = data.get('neighborhood', None)
        partnership_modify.id_user = data.get('id_admin', None)
        if not partnership_modify.id:
            raise BadRequest('Did not send partnership id to modify')
        if not partnership_modify.name:
            raise BadRequest('Name for partnership is mandatory')
        if not partnership_modify.address:
            raise BadRequest('Address for partnership is mandatory')
        if not partnership_modify.id_neighborhood:
            raise BadRequest('Neighborhood for partnership is mandatory')
        if not partnership_modify.id_user:
            raise BadRequest('Id User Admin for partnership is mandatory')

        try:
            partnership_query = Partnership.query.get(partnership_modify.id)
            partnership_query.name = partnership_modify.name
            partnership_query.address = partnership_modify.address
            partnership_query.id_neighborhood = partnership_modify.id_neighborhood
            partnership_query.id_user = partnership_modify.id_user
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable modify partnership')

        partnership_modify = Partnership.query.get(partnership_modify.id)
        the_partnerships = self.partnership_schema.dump(partnership_modify).data

        return jsonify({'partnerships': the_partnerships})

    @route('/partnership', methods=['DELETE'])
    def delete_partnership(self):
        params = request.args
        id_partnership = params.get('id_partnership', None)
        # HABRIA QUE PENSAR EN NO DEJAR ELIMINAR SI TIENE INFORMACION ASOCIADA (DPTOS CON INQUILINOS ACTIVOS, INFO
        # DE EXPENSAS ETC

        if not id_partnership:
            raise BadRequest('It is not allowed to delete all partnership')
        else:
            try:
                partnership_query = Partnership.query.get(id_partnership)
                partnership_delete = Partnership()
                partnership_delete.name = partnership_query.name
                db.session.delete(partnership_query)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print(str(e))
                raise InternalServerError('Unavailable delete partnership')

            return jsonify({'Partnership Delete': partnership_delete.name})

    @route('/neighborhood', methods=['GET'])
    def get_neighborhood(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_neighborhood = params.get('id_neighborhood', None)
        city_neighborhood = params.get('city', None)
        string = 'neighborhoods'

        neighborhoods = Neighborhoods.query
        if not id_neighborhood:
            neighborhoods = neighborhoods.filter(Neighborhoods.city == city_neighborhood)
            neighborhoods = neighborhoods.order_by(Neighborhoods.id).paginate(int(page), int(per_page), error_out=False)
            neighborhood_string = self.neighborhoods_schema.dump(neighborhoods).data
            #Para varios items, tener en cuenta usar el schema de pagination
        else:
            neighborhoods = neighborhoods.filter(Neighborhoods.id == id_neighborhood).first()
            neighborhood_string = self.neighborhood_schema.dump(neighborhoods).data
            string = "neighborhoods"

        return jsonify({string: neighborhood_string})

    @route('/neighborhood', methods=['POST'])
    def post_neighborhood(self):
        data = request.json
        neighborhood_obj = Neighborhoods()

        neighborhood_obj.name = data.get('name', None)
        if not neighborhood_obj.name:
            raise BadRequest('Name is mandatory')
        neighborhood_obj.city = data.get('city', None)
        if not neighborhood_obj.city:
            raise BadRequest('Name is mandatory')

        try:
            db.session.add(neighborhood_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store new neighborhood')

        neighborhood = Neighborhoods.query.filter(Neighborhoods.name == neighborhood_obj.name).first()
        neighborhood_data = self.neighborhood_schema.dump(neighborhood).data

        return jsonify({'neighborhood': neighborhood_data})

    @route('/neighborhood', methods=['DELETE'])
    def delete_neighborhood(self):
        params = request.args
        id_neighborhood_delete = params.get('neighborhood_delete', None)

        if not id_neighborhood_delete:
            raise BadRequest('It is not allowed to delete all neighborhood')
        else:
            try:
                neighborhood_query = Neighborhoods.query.get(id_neighborhood_delete)
                neighborhood_delete = Neighborhoods()
                neighborhood_delete.name = neighborhood_query.name
                db.session.delete(neighborhood_query)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print(str(e))
                raise InternalServerError('Unavailable delete neighborhood')

            return jsonify({'Neighborhood Delete': neighborhood_delete.name})
