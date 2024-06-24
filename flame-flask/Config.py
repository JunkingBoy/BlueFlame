from datetime import timedelta
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import yaml
import utils.StringUtil as StringUtil
from logging import Handler
import logging

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = StringUtil.generate_string(32)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_value_from_yaml("db_connect")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    appHandler: Handler = log()

    app.logger.addHandler(appHandler)
    app.logger.setLevel(logging.INFO)

    return app


def get_value_from_yaml(key):
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd)
    conf = "./config.yaml"
    with open(conf, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            print('-' * 80)
            return data.get(key)
        except yaml.YAMLError as e:
            print(e)
        finally:
            os.chdir(cwd)

def log() -> Handler:
    handler: Handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter: object = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    handler.setFormatter(formatter)

    return handler