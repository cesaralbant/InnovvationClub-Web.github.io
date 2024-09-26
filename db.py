from replit import db
from werkzeug.security import generate_password_hash

def init_db():
    if 'next_user_id' not in db:
        db['next_user_id'] = 1
    if 'next_blog_id' not in db:
        db['next_blog_id'] = 1
    if 'next_event_id' not in db:
        db['next_event_id'] = 1

    # Create an admin user if it doesn't exist
    if not db.get('user:admin'):
        db['user:admin'] = {
            'id': '0',
            'username': 'admin',
            'password': 'pbkdf2:sha256:260000$your_hashed_password_here',  # Replace with a secure hashed password
            'is_admin': True
        }
    
    # Create the pre-authorized user (cesar) if it doesn't exist
    if not db.get('user:cesar'):
        db['user:cesar'] = {
            'id': '1',
            'username': 'cesar',
            'password': generate_password_hash('cesar_password'),  # Replace 'cesar_password' with a secure password
            'is_admin': True
        }
