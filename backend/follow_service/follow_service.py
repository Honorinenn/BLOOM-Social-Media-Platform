# follow_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///follow.db'
db = SQLAlchemy(app)

class Follow(db.Model):
    follow_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, nullable=False)
    followee_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

db.create_all()

@app.route('/follow', methods=['POST'])
def follow():
    data = request.json
    follower_id = data['follower_id']
    followee_id = data['followee_id']
    existing_follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if existing_follow:
        return jsonify({'message': 'Already following'}), 400
    follow = Follow(follower_id=follower_id, followee_id=followee_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'Followed successfully'}), 200

@app.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.json
    follower_id = data['follower_id']
    followee_id = data['followee_id']
    follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'Unfollowed successfully'}), 200
    return jsonify({'message': 'Not following this user'}), 400

if __name__ == '__main__':
    app.run(port=5004)
