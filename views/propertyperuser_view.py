from flask_classy import FlaskView, route
from flask import jsonify, request

from schemas import PageOfRelationPropertyPerUserSchema
from schemas import PropertyPerUserSchema
from schemas import PageOfPropertyPerUserSchema
from model import PropertyPerUser, RelationPropertyPerUser, Partnership, Property
from schemas import PartnershipAdministratorSchema, PageOfPartnershipAdministratorSchema
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime

from schemas import RelationPropertyPerUserSchema


class PropertyPerUserView(FlaskView):
    route_base = '/propertyPerUser/'
    propertyPerUser_schema = PropertyPerUserSchema()
    propertiesPerUser_schema = PageOfPropertyPerUserSchema()
    relationPropertyPerUser_schema = RelationPropertyPerUserSchema()
    relationsPropertiesPerUser_schema = PageOfRelationPropertyPerUserSchema()
    partnership_per_admin = PartnershipAdministratorSchema()
    partnerships_per_admin = PageOfPartnershipAdministratorSchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        idUser = params.get('id_user', None)

        #propertiesPerUser_data = PropertyPerUser.query
        if not idUser:
            raise BadRequest('User ID is Mandatory')
        else:
            #prop = propertiesPerUser_data.join(Property).join(Partnership).add_columns(PropertyPerUser.id,
            #                                                                  PropertyPerUser.id_user,
            #                                                                  PropertyPerUser.id_property,
            #                                                                  Property.floor, Property.ph,
            #                                                                  Property.block, Property.lot,
            #                                                                  PropertyPerUser.id_relation,
            #                                                                  PropertyPerUser.date_created,
            #                                                                  PropertyPerUser.date_finished,
            #                                                                  Partnership.id, Partnership.name).\
            #                                                                  filter(PropertyPerUser.id_user == idUser)

            #prop = PropertyPerUser.query.filter(PropertyPerUser.id_user == idUser).join(Property).join(Partnership).\
            #    add_columns(PropertyPerUser.id, PropertyPerUser.id_user, PropertyPerUser.id_property,
            #    Property.floor, Property.ph, Property.block, Property.lot, PropertyPerUser.id_relation,
            #    PropertyPerUser.date_created, PropertyPerUser.date_finished, Partnership.id, Partnership.name)
            #propertiess = Property.query.join(Partnership).filter(Partnership.id == Property.id_partnership)
            #prop = PropertyPerUser.query.filter(PropertyPerUser.id_user == idUser).join(Property).\
            #    filter(PropertyPerUser.id_user == idUser)


            prop = PropertyPerUser.query.filter(PropertyPerUser.id_user == idUser)
                #.outerjoin(Property,
                #                                                    PropertyPerUser.id_property == Property.id)

            #prop = prop.outerjoin(Partnership, Property.id_partnership == Partnership.id)


            isTenant = prop.filter(PropertyPerUser.id_relation == 1)

            isOwner = prop.filter(PropertyPerUser.id_relation == 2)
            #isAdmin = properties.filter(PropertyPerUser.id_relation == 3)
            isOwnerHabitant = prop.filter(PropertyPerUser.id_relation == 4)


            isTenant = isTenant.order_by(PropertyPerUser.id.desc()).paginate(int(page), int(per_page),
                                                                                 error_out=False)

            isOwner = isOwner.order_by(PropertyPerUser.id.desc()).paginate(int(page), int(per_page),
                                                                                 error_out=False)
            #isAdmin = isAdmin.order_by(PropertyPerUser.id.desc()).paginate(int(page), int(per_page),
            #                                                                     error_out=False)
            isOwnerHabitant = isOwnerHabitant.order_by(PropertyPerUser.id.desc()).paginate(int(page), int(per_page),
                                                                                                 error_out=False)


            propertiesIsTenant_data = self.propertiesPerUser_schema.dump(isTenant).data
            propertiesIsOwner_data = self.propertiesPerUser_schema.dump(isOwner).data
            #propertiesIsAdmin_data = self.propertiesPerUser_schema.dump(isAdmin).data
            propertiesIsOwnerHabitant_data = self.propertiesPerUser_schema.dump(isOwnerHabitant).data

            return jsonify({'Inquilino': propertiesIsTenant_data, 'Propietario': propertiesIsOwner_data,
                            'Prop Habitante': propertiesIsOwnerHabitant_data})

        #Pensar en algun filtro para el caso de que un usuario sea admin e inquilino a la vez, para devolver en
        #objetos json diferentes. O el caso de usuarios propietarios e inquilinos

        #propertiesPerUser_data = self.propertiesPerUser_schema.dump(properties).data

        #return jsonify({'Propiedades': propertiesPerUser_data})

    def post(self):
        data = request.json
        propertyperuser_obj = PropertyPerUser()

        propertyperuser_obj.date_created = datetime.now()

        iduser = data.get('id_user', None)
        if not iduser:
            raise BadRequest('Id user is Mandatory')
        propiedad = data.get('id_property', None)
        if not propiedad:
            raise BadRequest('Id property is Mandatory')
        relation = data.get('id_relation', None)

        propertyperuser_obj.id_user = iduser
        propertyperuser_obj.id_property = propiedad
        if not relation:
            propertyperuser_obj.id_relation = None
        else:
            propertyperuser_obj.id_relation = relation

        propertyperuser_obj.date_finished = None

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

    def put(self):
        data = request.json
        propertiperuser = PropertyPerUser()
        propertiperuser.id = data.get('id', None)
        propertiperuser.id_user = data.get('id_user', None)
        propertiperuser.id_property = data.get('id_property', None)
        propertiperuser.id_relation = data.get('id_relation', None)
        activo = data.get('activo', None)

        if not propertiperuser.id:
            raise BadRequest('Did not send propertyPerUser id to modify')

        try:
            ppu_query = PropertyPerUser.query.get(propertiperuser.id)
            if propertiperuser.id_user:
                ppu_query.id_user = propertiperuser.id_user
            if propertiperuser.id_property:
                ppu_query.id_property = propertiperuser.id_property
            if propertiperuser.id_relation:
                ppu_query.id_relation = propertiperuser.id_relation
            if activo == 0:
                ppu_query.date_finished = datetime.now()

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable modify propertyPerUser')

        modifyPropertyPerUser = PropertyPerUser.query.get(propertiperuser.id)
        thepropertyperuser = self.propertyPerUser_schema.dump(modifyPropertyPerUser).data

        return jsonify({'Property Per User': thepropertyperuser})

    @route('/relation', methods=['POST'])
    def post_relation(self):
        data = request.json
        relation = RelationPropertyPerUser()
        relation.name = data.get('name', None)

        try:
            db.session.add(relation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store relation property per user')

        relations = RelationPropertyPerUser.query.order_by(RelationPropertyPerUser.id.desc()).first()
        relation = self.relationPropertyPerUser_schema.dump(relations).data

        return jsonify({'Relacion': relation})

    @route('/partnershipsAdmin', methods=['GET'])
    def get_partnership_admin(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_admin = params.get('admin', None)

        partnerships = Partnership.query
        if not id_admin:
            raise BadRequest('Admin id is Mandatory')
        else:
            partnerships = partnerships.filter(Partnership.id_user == id_admin)
            partnerships = partnerships.order_by(Partnership.name.desc()).paginate(int(page), int(per_page),
                                                                                 error_out=False)

        partnerships_data = self.partnerships_per_admin.dump(partnerships).data

        return jsonify({'Partnership': partnerships_data})
