# user_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class UserProfile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(255))
    website_url = db.Column(db.String(255))

db.create_all()

@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        return jsonify({
            'user_id': profile.user_id,
            'bio': profile.bio,
            'profile_picture_url': profile.profile_picture_url,
            'website_url': profile.website_url
        }), 200
    return jsonify({'message': 'Profile not found'}), 404

@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.json
    profile = UserProfile(
        user_id=data['user_id'],
        bio=data.get('bio', ''),
        profile_picture_url=data.get('profile_picture_url', ''),
        website_url=data.get('website_url', '')
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'Profile created successfully'}), 201

@app.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.json
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.bio = data.get('bio', profile.bio)
        profile.profile_picture_url = data.get('profile_picture_url', profile.profile_picture_url)
        profile.website_url = data.get('website_url', profile.website_url)
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    return jsonify({'message': 'Profile not found'}), 404

if __name__ == '__main__':
    app.run(port=5002)
