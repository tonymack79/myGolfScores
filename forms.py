from wtforms_alchemy import ModelForm
from models import User, Course, Score

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