from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.get_json()
        user = mongo.db.users.find_one({'username': data.get('username')})
        
        if user and check_password_hash(user['password'], data.get('password')):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify({'token': access_token}), 200
            
        return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        data = request.get_json()
        
        if mongo.db.users.find_one({'username': data.get('username')}):
            return jsonify({'error': 'Username already exists'}), 400
            
        if mongo.db.users.find_one({'email': data.get('email')}):
            return jsonify({'error': 'Email already exists'}), 400
            
        hashed_password = generate_password_hash(data.get('password'))
        user = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': hashed_password
        }
        
        mongo.db.users.insert_one(user)
        return jsonify({'message': 'User created successfully'}), 201
