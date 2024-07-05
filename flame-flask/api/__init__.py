from flask import Flask
from .User import bf_user
from .CaseTemplateParse import case_parse 
from .Project import project


def register_routes(app: Flask):
    app.register_blueprint(bf_user, url_prefix="/user/")
    app.register_blueprint(case_parse, url_prefix="/case/parse/")
    app.register_blueprint(project, url_prefix="/project/")
