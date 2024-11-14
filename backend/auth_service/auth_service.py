# auth_service.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import jwt
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    totp_secret = db.Column(db.String(255))

db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    totp_secret = pyotp.random_base32()
    user = User(username=username, email=email, password_hash=password, totp_secret=totp_secret)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'totp_secret': totp_secret})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    totp_code = data.get('totp_code')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(totp_code):
            token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'message': 'Login successful', 'token': token})
        else:
            return jsonify({'message': 'Invalid TOTP code'}), 401
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=5001)
