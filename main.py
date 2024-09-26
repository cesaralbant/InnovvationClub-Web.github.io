from flask import Flask, render_template
from flask_login import LoginManager
from auth import auth_bp, init_app as init_auth
from admin import admin_bp
from blog import blog_bp
from events import events_bp
from db import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(events_bp)

# Initialize the database
init_db()

# Initialize authentication
init_auth(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
