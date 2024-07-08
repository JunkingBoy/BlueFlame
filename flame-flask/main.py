from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask
from Config import create_app
from model import db
from api import register_routes


if __name__ == "__main__":
    app: Flask = create_app()
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    register_routes(app)
    with app.app_context():
        # 在定义表之前，打印出SQLAlchemy的元数据，以确保所有表都已注册
        print('-'*80)
        print(db.metadata.tables, sep="\n")
        print('-'*80)
        db.create_all()

    app.run(host='0.0.0.0', port=8000, debug=True)
