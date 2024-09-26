from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')
        
        if action == 'delete':
            db.delete(f"user:{user_id}")
            flash('User deleted successfully.')
        elif action == 'edit':
            username = request.form.get('username')
            is_admin = request.form.get('is_admin') == 'on'
            user_data = db.get(f"user:{user_id}")
            if user_data:
                user_data['username'] = username
                user_data['is_admin'] = is_admin
                db.set(f"user:{user_id}", user_data)
                flash('User updated successfully.')
    
    users = [db.get(key) for key in db.prefix('user:')]
    return render_template('admin/users.html', users=users)

@admin_bp.route('/blogs')
@login_required
def blogs():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    blogs = [db.get(key) for key in db.prefix('blog:')]
    return render_template('admin/blogs.html', blogs=blogs)

@admin_bp.route('/events')
@login_required
def events():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    events = [db.get(key) for key in db.prefix('event:')]
    return render_template('admin/events.html', events=events)
