from flask import Flask
from .User import user
from .CaseTemplateParse import case_parse 
from .Project import project


def register_routes(app: Flask):
    app.register_blueprint(user, url_prefix="/user/")
    app.register_blueprint(case_parse, url_prefix="/case/parse/")
    app.register_blueprint(project, url_prefix="/project/")
