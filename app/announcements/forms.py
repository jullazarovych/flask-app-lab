from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.announcements.models import Topic

class AnnouncementForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    topics = SelectMultipleField('Topics', coerce=int)  # Поле для вибору кількох тем
    submit = SubmitField('Create Announcement')

    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.topics.choices = [(topic.id, topic.name) for topic in Topic.query.all()]


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    sort_by = SelectField('Sort By', choices=[
        ('name', 'Name'),
        ('created_at', 'Created At')
    ])
    submit = SubmitField('Search')