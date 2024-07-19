from flask import Flask
from . import User


def register_routes(app: Flask):
    app.register_blueprint(User.bp, url_prefix="/user/")
    # app.register_blueprint(CaseTemplateParse.bp, url_prefix="/case/parse/")
    # app.register_blueprint(Project.bp, url_prefix="/project/")
