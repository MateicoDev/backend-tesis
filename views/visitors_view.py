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
        visitor_data  = self.visitor_schema.dump(visitor_save).data

        return jsonify({'Visitor': visitor_data})


class EventView(FlaskView):
    route_base = '/events/'
    event_schema = EventSchema()
    events_schema = PageOfEventSchema()

    @route('/', methods=['GET'])
    def get(self):
        params = request.args
        #page = params.get('page', 1)
        #per_page = params.get('per_page', 10)
        id_event = params.get('id_event', None)

        if not id_event:
            raise BadRequest('Event id is Mandatory')
        else:
            event = Event.query.get(id_event)
            #event = event.paginate(int(page), int(per_page), error_out=False)

        event_data = self.event_schema.dump(event).data

        return jsonify({'Evento': event_data})

    @route('/', methods=['POST'])
    def post(self):
        data = request.json
        event_obj = Event()

        event_obj.id_partnership = data.get('id_partnership', None)
        if not event_obj.id_partnership:
            raise BadRequest('Partnership is Mandatory')
        event_obj.hour_since = data.get('hour_since', None)
        if not event_obj.hour_since:
            raise BadRequest('Hour since is Mandatory')
        event_obj.hour_until = data.get('hour_until', None)
        if not event_obj.hour_until:
            raise BadRequest('Hour until is Mandatory', None)
        event_obj.id_user = data.get('id_user', None)
        if not event_obj.id_user:
            raise BadRequest('User id is Mandatory', None)

        try:
            db.session.add(event_obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unable to store a new Visitor')

        event_save = Event.query.order_by(Event.id.desc()).first()
        event_save = self.event_schema.dump(event_save).data

        return jsonify({'Event': event_save})





