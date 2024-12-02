from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active post')
    publish_date = DateField('Publish date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField('Tags', coerce=int)
    submit = SubmitField('Add post')

