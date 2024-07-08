from flask import Flask
from .User import bf_user
from .CaseTemplateParse import bf_case_parse 
from .Project import bf_project


def register_routes(app: Flask):
    app.register_blueprint(bf_user, url_prefix="/user/")
    app.register_blueprint(bf_case_parse, url_prefix="/case/parse/")
    app.register_blueprint(bf_project, url_prefix="/project/")
