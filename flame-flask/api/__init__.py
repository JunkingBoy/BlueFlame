from flask import Flask
from . import User, CaseTemplateParse, Project, Plan


def register_routes(app: Flask):
    app.register_blueprint(User.bp, url_prefix="/user/")
    app.register_blueprint(CaseTemplateParse.bp, url_prefix="/case/parse/")
    app.register_blueprint(Project.bp, url_prefix="/project/")
    app.register_blueprint(Plan.bp, url_prefix="/project/")
