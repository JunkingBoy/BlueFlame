'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-22 03:53:37
Description: 
'''
from flask import Flask

from . import User, CaseTemplateParse, Project

def register_routes(app: Flask):
    app.register_blueprint(User.bp, url_prefix="/user/")
    app.register_blueprint(CaseTemplateParse.bp, url_prefix="/case/parse/")
    app.register_blueprint(Project.bp, url_prefix="/project/")
