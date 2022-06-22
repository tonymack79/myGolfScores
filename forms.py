from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired
from models import db, Course, Score

class SignupForm(FlaskForm):
    """Form for adding a user"""
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Form for logging in a user"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class CourseForm(FlaskForm):
    """Form for adding a golf course"""
    course_name = StringField("Course Name", validators=[DataRequired()])
    par = IntegerField("Par", validators=[DataRequired()])

class ScoreForm(FlaskForm):
    """Form for adding golf score"""
    score = IntegerField("Score", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
