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