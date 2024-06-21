from flask import Flask
from .User import user


def register_routes(app:Flask): 
    app.register_blueprint(user)
