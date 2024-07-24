from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask, current_app
from Config import create_app
from model import db
from api import register_routes


if __name__ == "__main__":
    app: Flask = create_app()
    CORS(app)
    JWTManager(app)
    # todo需要修改
    db.init_app(app)
    register_routes(app)
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        current_app.logger.error(f"Error creating database tables: {e}")

    app.run(host='0.0.0.0', port=8000, debug=True)
