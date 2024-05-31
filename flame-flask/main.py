from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .api.User import users
from .api.Crypt import crypt

app: object = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'VeryS3cr3tK3yWithNum83rs&Spec!alChar'  # 应该更换为安全的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
CORS(app=app)
jwt: object = JWTManager(app=app)

# 注册蓝图
app.register_blueprint(users)
app.register_blueprint(crypt)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
