from flask import Flask
from .User import user
from .CaseTemplateParse import case


def register_routes(app: Flask):
    app.register_blueprint(user, url_prefix="/user/")
    app.register_blueprint(case)
