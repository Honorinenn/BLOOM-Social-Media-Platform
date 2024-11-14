# post_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Like(db.Model):
    like_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

db.create_all()

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    post = Post(user_id=data['user_id'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully', 'post_id': post.post_id}), 201

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    comment = Comment(post_id=post_id, user_id=data['user_id'], content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully', 'comment_id': comment.comment_id}), 201

@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.json
    existing_like = Like.query.filter_by(post_id=post_id, user_id=data['user_id']).first()
    if existing_like:
        return jsonify({'message': 'Already liked'}), 400
    like = Like(post_id=post_id, user_id=data['user_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked'}), 201

if __name__ == '__main__':
    app.run(port=5003)
