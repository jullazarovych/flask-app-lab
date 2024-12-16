from flask import render_template, redirect, url_for, flash, request, abort
from app import db
from . import announce_bp
from app.announcements.models import Announcement, Topic
from app.announcements.forms import AnnouncementForm
from app import login_manager
from flask_login import login_user, logout_user, current_user, login_required

@announce_bp.route('/add', methods=['GET', 'POST'])
def create_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id 
        )
        selected_topics = Topic.query.filter(Topic.id.in_(form.topics.data)).all()
        announcement.topics.extend(selected_topics)
        db.session.add(announcement)
        db.session.commit()

        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announce.create_announcement'))
    
    return render_template('add_ann.html', form=form)


@announce_bp.route('/anns', methods=['GET', 'POST'])
def announcements():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')

    query = Announcement.query

    if search_query:
        query = query.filter(Announcement.name.ilike(f'%{search_query}%'))

    if sort_order == 'desc':
        query = query.order_by(getattr(Announcement, sort_by).desc())
    else:
        query = query.order_by(getattr(Announcement, sort_by).asc())

    announcements = query.all()
    return render_template('anns.html', announcements=announcements, search_query=search_query, sort_by=sort_by, sort_order=sort_order)


@announce_bp.route('/<int:id>')
def announcement_detail(id):
    announcement = Announcement.query.get_or_404(id)
    return render_template('detail_ann.html', announcement=announcement)


@announce_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    if announcement.user_id != current_user.id:
        abort(403)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted successfully', 'success')
    return redirect(url_for('announce.announcements'))

@announce_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    announcement = Announcement.query.get_or_404(id)

    if announcement.user_id != current_user.id:
        abort(403) 

    if request.method == 'POST':
        announcement.name = request.form['name']
        announcement.description = request.form['description']

        db.session.commit()
        flash('Announcement updated successfully', 'success')
        return redirect(url_for('announce.announcement_detail', id=announcement.id))

    return render_template('edit_announcement.html', announcement=announcement)