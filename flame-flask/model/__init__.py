from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy(
    engine_options={"connect_args": {
        "options": "-c timezone=Asia/Shanghai"
    }})
