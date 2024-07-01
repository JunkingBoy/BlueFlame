from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy(
    engine_options={"connect_args": {
        "options": "-c timezone=utc"
    }})


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    print("SETTING TIMEZONE")
    cursor.execute("SET timezone TO 'UTC';")
    cursor.close()
