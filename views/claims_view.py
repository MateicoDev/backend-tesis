from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import PageOfClaimsSchema, ClaimTypeSchema
from model import Claim
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden
from datetime import datetime


class ClaimsView(FlaskView):
    route_base = '/claims/'
    claims_schema = PageOfClaimsSchema()
    claim_type_schema = ClaimTypeSchema()

    # @route(route_base, methods=['GET'])
    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        category = params.get('category', None)

        claims_data = Claim.query
        if category is None:
            claims_data = claims_data.filter(Claim.status == 1)
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        else:
            claims_data = claims_data.filter(Claim.status == 1, Claim.category == category)
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        claims_data = self.recipe_schema.dump(claims).data

        return jsonify(claims_data)

    def post(self):
        data = request.json
        claim_obj = Claim()
        claim_obj.date = datetime.now()
        claim_obj.title = data.get('title', None)
        claim_obj.content = data.get('content', None)
        claim_obj.category = data.get('category', None)
        claim_obj.status = data.get('status', None)
        
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
