from database import db, create_app
from werkzeug.exceptions import *
from flask import jsonify
from views import *
import os

API_PREFIX = "/api/v1"

application = create_app()


@application.errorhandler(401)
@application.errorhandler(404)
@application.errorhandler(403)
@application.errorhandler(412)
@application.errorhandler(400)
@application.errorhandler(500)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e), message=e.description), code


@application.teardown_appcontext
def shutdown_session(response_or_exc):
    try:
        if response_or_exc is None:
            db.session.commit()
    finally:
        db.session.remove()
    return response_or_exc


@application.route("/ping")
def hello():
    return jsonify(message="Pong!"), 200


if __name__ == '__main__':
    with application.app_context():
        db.create_all()
        application.run(host=os.getenv("APP_HOST", "0.0.0.0"), port=os.getenv("PORT", 5000))
