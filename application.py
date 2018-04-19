from database import db,create_app
from werkzeug.exceptions import *
from views import *
from flask_cors import CORS
from flask import jsonify
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
        application.run(host=os.getenv("APP_HOST", "0.0.0.0"), port=os.getenv("APP_PORT", 5000))
