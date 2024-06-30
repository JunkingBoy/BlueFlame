'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-01 19:32:30
Description: 
'''
from datetime import timedelta
import os
from typing import Any
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import yaml
import utils.StringUtil as StringUtil
from logging import Handler
from sqlalchemy.engine.url import URL
from sqlalchemy.util import immutabledict
import logging

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = StringUtil.generate_string(32)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    # 根据Docker环境变量设置数据库URI
    if os.getenv('DOCKER_ENV') == 'true':
        app.config['SQLALCHEMY_DATABASE_URI'] = URL(
            drivername=os.getenv("DB_DRIVER"),
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT")),
            query={"options": "-c TimeZone=Asia/Shanghai"}
        )
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = URL(
            drivername=get_value_from_yaml('db_driver'),
            username=get_value_from_yaml("db_user"),
            password=get_value_from_yaml("db_password"),
            host=get_value_from_yaml("db_host"),
            database=get_value_from_yaml("db_name"),
            port=get_value_from_yaml("db_port"),
            query={"options": "-c Asia/Shanghai"}
        )


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    appHandler: Handler = log()

    app.logger.addHandler(appHandler)
    app.logger.setLevel(logging.INFO)

    return app


def get_value_from_yaml(key) -> Any:
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd)
    conf = "./config.yaml"
    with open(conf, 'r', encoding='utf-8') as stream:
        try:
            data = yaml.safe_load(stream)
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
