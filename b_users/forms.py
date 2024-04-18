from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User


class SignupForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Last Name"})
    email_id = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Email Id"})
    password = PasswordField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Password"})

class SigninForm(FlaskForm):
    email_id = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Email Id"})
    password = PasswordField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Password"})
    
    
class UserForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[InputRequired(), Length(min=3, max=30)], render_kw={"placeholder": "Last Name"})
    email_id = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Email Id"})


