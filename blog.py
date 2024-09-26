from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog')
def blog_list():
    blogs = [db.get(key) for key in db.prefix('blog:')]
    return render_template('blog.html', blogs=blogs)

@blog_bp.route('/blog/<int:blog_id>')
def blog_post(blog_id):
    blog = db.get(f"blog:{blog_id}")
    if blog:
        return render_template('blog_post.html', blog=blog)
    flash('Blog post not found')
    return redirect(url_for('blog.blog_list'))

@blog_bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        blog_id = str(db.get('next_blog_id', 1))
        db.set('next_blog_id', int(blog_id) + 1)
        db.set(f"blog:{blog_id}", {
            'id': blog_id,
            'title': title,
            'content': content,
            'author': current_user.username
        })
        flash('Blog post created successfully')
        return redirect(url_for('blog.blog_post', blog_id=blog_id))
    return render_template('blog_post.html', new=True)
