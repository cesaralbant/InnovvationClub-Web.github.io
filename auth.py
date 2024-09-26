from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from db import db

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class User(UserMixin):
    def __init__(self, id, username, password, is_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    user_data = db.get(f"user:{user_id}")
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password'], user_data['is_admin'])
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = db.get(f"user:{username}")
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['username'], user_data['password'], user_data['is_admin'])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if db.get(f"user:{username}"):
            flash('Username already exists')
        else:
            user_id = str(db.get('next_user_id', 1))
            db.set('next_user_id', int(user_id) + 1)
            db.set(f"user:{username}", {
                'id': user_id,
                'username': username,
                'password': generate_password_hash(password),
                'is_admin': False
            })
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/crew', methods=['GET', 'POST'])
def crew():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = db.get(f"user:{username}")
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['username'], user_data['password'], user_data['is_admin'])
            login_user(user)
            if username == 'cesar':
                user.is_admin = True
                db.set(f"user:{username}", {
                    'id': user.id,
                    'username': user.username,
                    'password': user.password,
                    'is_admin': True
                })
            return redirect(url_for('index'))
        else:
            flash('Invalid crew credentials')
    return render_template('crew.html')

def init_app(app):
    login_manager.init_app(app)
