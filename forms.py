from flask_wtf import FlaskForm
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

class LoginForm(ModelForm):
    """Form for logging in a user"""
    class Meta:
        model = User
        only = ['username', 'password']

class CourseForm(ModelForm):
    """Form for adding a golf course"""
    class Meta:
        model = Course

class ScoreForm(ModelForm):
    """Form for adding golf score"""
    class Meta:
        model = Score