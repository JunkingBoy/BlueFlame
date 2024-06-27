from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask
from Config import create_app
from model import db
from api import register_routes

app: Flask = create_app()
CORS(app)
JWTManager(app)
db.init_app(app)
register_routes(app)

@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
