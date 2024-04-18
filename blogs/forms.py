from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, StringField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .models import Blogs, Category


class BlogForm(FlaskForm):
    # img= ImageField(validators = InputRequired(), render_kw={"placeholder": "Image Upload"})
    title = StringField(validators=[InputRequired(),], render_kw={"placeholder": "Blog Title"})
    category = SelectField('Category', choices=[(cat.name, cat.value) for cat in Category], validators=[InputRequired()])
    blog_content = StringField(validators=[InputRequired(),], render_kw={"placeholder": "Blog Content"})
    # img = FileField(validators=[FileRequired('File was empty!')])
    img = FileField()
    submit = SubmitField('Submit Entry')