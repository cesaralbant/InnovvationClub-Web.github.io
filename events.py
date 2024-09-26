from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def events_list():
    events = [db.get(key) for key in db.prefix('event:')]
    return render_template('events.html', events=events)

@events_bp.route('/events/new', methods=['GET', 'POST'])
@login_required
def new_event():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        description = request.form.get('description')
        event_id = str(db.get('next_event_id', 1))
        db.set('next_event_id', int(event_id) + 1)
        db.set(f"event:{event_id}", {
            'id': event_id,
            'title': title,
            'date': date,
            'description': description,
            'organizer': current_user.username
        })
        flash('Event created successfully')
        return redirect(url_for('events.events_list'))
    return render_template('events.html', new=True)
