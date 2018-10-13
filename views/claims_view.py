from flask_classy import FlaskView, route
from flask import jsonify, request
from schemas import PageOfClaimsSchema, ClaimTypeSchema, ClaimSchema, ClaimMessagesSchema, PageOfClaimsMessagesSchema
from model import Claim, ClaimType, ClaimStatus, ClaimMessages
from database import db
from werkzeug.exceptions import InternalServerError, BadRequest
from datetime import datetime


class ClaimsView(FlaskView):
    route_base = '/claims/'
    claims_schema = PageOfClaimsSchema()
    claims_type_schema = ClaimTypeSchema()
    claim_schema = ClaimSchema()
    claim_messages_schema = ClaimMessagesSchema()
    claims_messages_schema = PageOfClaimsMessagesSchema()

    # @route(route_base, methods=['GET'])
    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_user_reciver = params.get('id_user_reciver', None)
        id_user_sender = params.get('id_user_sender', None)

        claims_data = Claim.query
        if id_user_reciver is not None:
            claims_data = claims_data
            claims = claims_data.filter(Claim.id_user_reciver == id_user_reciver)
            claims = claims.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        elif id_user_sender is not None:
            claims_data = claims_data
            claims = claims_data.filter(Claim.id_user_sender == id_user_sender)
            claims = claims.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        else:
            claims = claims_data.order_by(Claim.date.desc()).paginate(int(page), int(per_page), error_out=False)
        claims_data = self.claims_schema.dump(claims).data

        return jsonify({'claims': claims_data})

    def post(self):
        # owner = authenticator.basic_auth(request.authorization, "CreateCLAIM")
        # valid_users = []
        data = request.json
        claim_obj = Claim()

        claim_obj.date = datetime.now()

        user_reciver = data.get('user_reciver', None)
        if not user_reciver:
            raise BadRequest('User reciver is Mandatory')
        claim_obj.id_user_reciver = user_reciver.get('id_user', None)
        if not claim_obj.id_user_reciver:
            raise BadRequest('Id of reciver is Mandatory')
        user_sender = data.get('user_sender', None)
        if not user_sender:
            raise BadRequest('User sender is Mandatory')
        claim_obj.id_user_sender = user_sender.get('id_user', None)
        if not claim_obj.id_user_sender:
            raise BadRequest('Id of sender is Mandatory')
        claim_obj.title = data.get('title', None)
        if not claim_obj.title:
            raise BadRequest('Claim title is Mandatory')
        claim_obj.subject = data.get('subject', None)
        if not claim_obj.subject:
            raise BadRequest('Claim subject is Mandatory')
        claim_obj.id_property = data.get('id_property', None)
        if not claim_obj.id_property:
            raise BadRequest('Id property is Mandatory')
        claim_obj.id_partnership = data.get('id_partnership', None)
        if not claim_obj.id_property:
            raise BadRequest('Id partnership is Mandatory')

        claim_obj.picture = data.get('picture', None)

        category = data.get('category', None)
        if not category:
            raise BadRequest('Claim category is Mandatory')
        claim_obj.id_category = category.get('id', None)
        if not claim_obj.id_category:
            raise BadRequest('Claim category is Mandatory')

        type_claim = ClaimStatus.query
        type_claim = type_claim.filter(ClaimStatus.name == 'Creada').first_or_404()
        claim_obj.id_status = type_claim.id

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

    def delete(self):
        params = request.args
        id_claim_delete = params.get('id_claim', None)

        if not id_claim_delete:
            raise BadRequest('It is not allowed to delete all claim')
        else:
            try:
                claim_query = Claim.query.filter(Claim.id == id_claim_delete).first()
                claim_delete = claim_query
                #claim_status = ClaimStatus.query
                #claim_status = claim_status.filter(ClaimStatus.id == claim_query.id_status)
                claim_status = ClaimStatus.query.filter(ClaimStatus.id == claim_query.id_status).first()

                if claim_status.name == 'Creada':
                    db.session.delete(claim_query)
                    db.session.commit()
                else:
                        return jsonify({'error': 'Only requests that have not been addressed can be removed'})
            except Exception as e:
                db.session.rollback()
                print(str(e))
                raise InternalServerError('Unavailable delete claim')

            return jsonify({'Claim Delete': claim_delete.title})

    @route('/messages', methods=['POST'])
    def post_messages(self):
        data = request.json
        claim_message = ClaimMessages()
        claim_message.date = datetime.now()
        claim_message.id_user = data.get('id_user', None)
        if not claim_message.id_user:
            raise BadRequest('Id user is Mandatory')
        claim_message.id_partnership = data.get('id_partnership', None)
        if not claim_message.id_partnership:
            raise BadRequest('Id partnetship is Mandatory')
        claim_message.comment = data.get('comment', None)
        if not claim_message.comment:
            raise BadRequest('Claim comment is Mandatory')

        claim = data.get('claim', None)
        if not claim:
            raise BadRequest('Claim is Mandatory')
        claim_message.id_claim = claim.get('id', None)
        if not claim_message.id_claim:
            raise BadRequest('Claim id is Mandatory')

        claim_id = Claim.query
        claim_id = claim_id.filter(Claim.id == claim_message.id_claim)
        claim_id = claim_id.order_by(Claim.date.desc()).first_or_404()
        if not claim_id:
            raise BadRequest('Claim id not exist')

        if not claim_id.id_partnership == claim_message.id_partnership:
            raise BadRequest('Id partnership not its the same in the claim')
        # if not claim_id. == claim_message.id_user_sender:
        #     raise BadRequest('Id user not its the same in the claim')

        # send_notification(valid_users, NOTIFICATION_TITLE_CLAIM_MESSAGE, NOTIFICATION_BODY_CLAIM_MESSAGE
        #                   .format(owner.user_name), ID_NOTIFICATION_TYPE_CLAIM_MESSAGE,
        #                   owner.user_profile_pic, notification_type=CLAIM_MESSAGE)

        try:
            db.session.add(claim_message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store new message in the claim for user')

        claim = ClaimMessages.query.order_by(ClaimMessages.date.desc()).first()
        claim_messages_data = self.claim_messages_schema.dump(claim).data

        return jsonify({'claim_messages': claim_messages_data})

    @route('/messages', methods=['GET'])
    def get_messages(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        category = params.get('category', None)

        id_claim = params.get('id', None)
        if not id_claim:
            raise BadRequest('Claim id is Mandatory')

        claims_messages_data = ClaimMessages.query
        if category is None:
            claims_messages = claims_messages_data.filter(ClaimMessages.id_claim == id_claim)
            claims_messages = claims_messages.order_by(ClaimMessages.date.asc()).paginate(int(page), int(per_page),
                                                                                          error_out=False)
        else:
            claims_messages_data = claims_messages_data.filter(Claim.category == category)
            claims_messages = claims_messages_data.order_by(Claim.date.asc()).paginate(int(page), int(per_page),
                                                                                       error_out=False)

        claims_messages_data = self.claims_messages_schema.dump(claims_messages).data

        return jsonify({'claim_messages': claims_messages_data})

    @route('/types', methods=['POST'])
    def post_types(self):
        data = request.json
        claim_types = ClaimType()
        claim_types.name = data.get('name', None)
        if not claim_types.name:
            raise BadRequest('Name for Type of claim is Mandatory')

        try:
            db.session.add(claim_types)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store type of claim for user')

        claim_types = ClaimType.query.order_by(ClaimType.id.desc()).first()
        types_of_claims = self.claims_type_schema.dump(claim_types).data

        return jsonify({'claim_types': types_of_claims})

    @route('/types', methods=['GET'])
    def get_types(self):

        claims_types_data = ClaimType.query
        claims_types = claims_types_data.order_by(ClaimType.name.asc()).all()
        types_of_claims = self.claims_type_schema.dump(claims_types, many=True).data

        return jsonify({'claim_types': types_of_claims})

    @route('/types', methods=['PUT'])
    def put_type(self):
        data = request.json
        claim_types = ClaimType()
        claim_types.id = data.get('id', None)
        claim_types.name = data.get('name', None)
        if not claim_types.id:
            raise BadRequest('Did not send claim id to modify')

        try:
            claim_type_query = ClaimType.query.get(claim_types.id)
            claim_type_query.name = claim_types.name
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable modify type of claim')

        claim_types = ClaimType.query.get(claim_types.id)
        types_of_claims = self.claims_type_schema.dump(claim_types).data

        return jsonify({'claim_types': types_of_claims})


