from flask_classy import FlaskView, route
from flask import jsonify, request

from schemas import VisitorPerEventSchema, VisitorSchema, EventSchema
from schemas import PageOfVisitorSchema, PageOfVisitorPerEventSchema, PageOfEventSchema
from model import Visitor, VisitorPerEvent, Event

from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime

class VisitorView(FlaskView):
    route_base = "/visitors"
    visitor_schema = VisitorSchema()
    visitors_schema = PageOfVisitorSchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        dni_visitor = params.get('dni', None)

        visitante = Visitor.query
        if not dni_visitor:
            raise BadRequest('Dni of visitor is Mandatory')
        else:
            visitantes = visitante.filter(Visitor.dni == dni_visitor)
            #Se tiene en cuenta que hay mas de una persona con el mismo DNI en Argentina
            visitantes = visitantes.order_by(Visitor.id.asc()).paginate(int(page), int(per_page), error_out=False)

        visitantes_data = self.visitors_schema.dump(visitantes).data

        return jsonify({'Visitantes' : visitantes_data})

    def post(self):
        data = request.json
        visitor_obj = Visitor()

        visitor_obj.name = data.get('name', None)
        if not visitor_obj.name:
            raise BadRequest('Visitor name is Mandatory')
        visitor_obj.lastname = data.get('lastname', None)
        if not visitor_obj.lastname:
            raise BadRequest('Visitor lastname is Mandatory')
        visitor_obj.dni = data.get('dni', None)
        if not visitor_obj.dni:
            raise BadRequest('Visitor Dni is Mandatory')
        visitor_obj.sex = data.get('sex', None)
        if not visitor_obj.sex:
            raise BadRequest('Visitor sex is Mandatory')

        try:
            db.session.add(visitor_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store a new Visitor')

        visitor_save = Visitor.query.order_by(Visitor.id.desc()).first()
        visitor_data  = self.visitor_schema.dump(visitor_save)

        return jsonify({'Visitor': visitor_data})

#class EventView(FlaskView):
 #   route_base = "/VisitorPerEvent/"
  #  event_schema = EventSchema()
   # events_schema = PageOfEventSchema()

    #@route('/event', methods=['GET'])
    #def get(self):
     #   params = request.args
      #  page = params.get('page', 1)
       # per_page = params.get('per_page', 10)
        #partnership = params.get('id_partnership', None)


