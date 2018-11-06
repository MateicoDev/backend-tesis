from database import create_app, db
from werkzeug.exceptions import *
from views import *
from flask_cors import CORS
from flask import jsonify
from populators.claim_initializer import ClaimInitializer
from populators.users_initializer import UsersInitializer
from populators.property_initializer import PropertyInitializer
from populators.propertyPerUser_initializer import PropertyPerUserInitializer
import os

application = create_app()


@application.errorhandler(401)
@application.errorhandler(404)
@application.errorhandler(403)
@application.errorhandler(409)
@application.errorhandler(412)
@application.errorhandler(400)
@application.errorhandler(500)
@application.errorhandler(501)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


api_prefix = "/api/v1"
ClaimsView.register(application, route_prefix=api_prefix)
UsersView.register(application, route_prefix=api_prefix)
PartnershipView.register(application, route_prefix=api_prefix)
PropertyView.register(application, route_prefix=api_prefix)
LoginView.register(application, route_prefix=api_prefix)
PropertyPerUserView.register(application, route_prefix=api_prefix)
VisitorView.register(application, route_prefix=api_prefix)
EventView.register(application, route_prefix=api_prefix)
VisitorPerEventView.register(application, route_prefix=api_prefix)
ExpensesView.register(application, route_prefix=api_prefix)

@application.teardown_appcontext
def shutdown_session(response_or_exc):
    try:
        if response_or_exc is None:
            db.session.commit()
    finally:
        db.session.remove()
    return response_or_exc


if __name__ == '__main__':
    with application.app_context():
        CORS(application)
        db.create_all()
        ClaimInitializer().init_status_claims()
        ClaimInitializer().init_type_claims()
        UsersInitializer().init_users()
        PropertyInitializer().init_neighborhoods()
        PropertyInitializer().init_partnership()
        PropertyInitializer().init_properties()
        PropertyPerUserInitializer().init_relation_propertyPerUser()
        PropertyPerUserInitializer().init_propertyPerUser()
        application.run(host=os.getenv("APP_HOST", "0.0.0.0"), port=os.getenv("PORT", 5000))
