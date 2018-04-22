from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import PageOfClaimsSchema, ClaimTypeSchema, ClaimSchema
from model import Claim, ClaimType, ClaimStatus
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class ClaimsView(FlaskView):
    route_base = '/claims/'
    claims_schema = PageOfClaimsSchema()
    claim_type_schema = ClaimTypeSchema()
    claim_schema = ClaimSchema()

    # @route(route_base, methods=['GET'])
    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        category = params.get('category', None)
        status = params.get('status', None)

        claims_data = Claim.query
        if category is None and status is None:
            claims_data = claims_data#.filter(Claim.status)
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        elif category is None:
            claims_data = claims_data.filter(not Claim.status)
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        else:
            claims_data = claims_data.filter(Claim.status, Claim.category == category)
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        claims_data = self.claims_schema.dump(claims).data

        return jsonify(claims_data)

    def post(self):
        data = request.json
        claim_obj = Claim()
        claim_obj.date = datetime.now()
        claim_obj.title = data.get('title', None)
        if not claim_obj.title:
            raise BadRequest('Claim title is Mandatory')
        claim_obj.content = data.get('content', None)
        if not claim_obj.content:
            raise BadRequest('Claim content is Mandatory')
        claim_obj.id_category = data.get('id_category', None)
        if not claim_obj.id_category:
            raise BadRequest('Claim id_category is Mandatory')

        type_claim = ClaimStatus.query
        type_claim = type_claim.filter(ClaimStatus.name == 'CREADA').first_or_404()
        claim_obj.id_status = type_claim.id
        claim_obj.dni_sender = "38332661"
        claim_obj.type_dni_sender = "DNI"
        claim_obj.id_property = 1
        claim_obj.id_partnership = 1

        try:
            db.session.add(claim_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store new claim for user ')

        claim = Claim.query.order_by(Claim.date.desc()).first()
        claim_data = self.claim_schema.dump(claim).data

        return jsonify({'claim': claim_data})
