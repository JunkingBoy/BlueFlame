from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

from .api.User import users
from .api.Crypt import crypt

app: object = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'VeryS3cr3tK3yWithNum83rs&Spec!alChar'  # 应该更换为安全的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# 配置数据库URI，格式为：postgresql://<username>:<password>@<hostname>/<database_name>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app=app)
jwt: object = JWTManager(app=app)

# 注册蓝图
app.register_blueprint(users)
app.register_blueprint(crypt)

# 初始化SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'username: {self.username}, email: {self.email}' 

@app.route('/users_test', methods=['GET'])
def get_users():
    with app.app_context():
        users = User.query.all()
        return jsonify([user.username for user in users])

if __name__ == '__main__':
    app.run(port=8000, debug=True)
