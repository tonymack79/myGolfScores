from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from wtforms_alchemy import model_form_factory
from models import db, User, Course, Score

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class UserAddForm(ModelForm):
    """Form for adding a user"""
    class Meta:
        model = User

class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class CourseForm(ModelForm):
    """Form for adding a golf course"""
    class Meta:
        model = Course

class ScoreForm(ModelForm):
    """Form for adding golf score"""
    class Meta:
        model = Score
