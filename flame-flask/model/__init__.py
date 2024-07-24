'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-24 22:25:56
Description: 
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy(
    engine_options={"connect_args": {
        "options": "-c timezone=Asia/Shanghai"
    }})
