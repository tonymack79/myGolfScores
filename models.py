from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connects database to Flask app"""
    
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Class for creating a user model"""

    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.Text,
                         unique=True,
                         nullable=False,
                        #  max length
                         )
    
    first_name = db.Column(db.Text,
                           nullable=False)
    
    last_name = db.Column(db.Text,
                           nullable=False)

class Course(db.Model):
    """Class for adding a golf course"""
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    course_name = db.Column(db.Text,
                            nullable=False)
    
    par = db.Column(db.Integer,
                    nullable=False)
    
    rating = db.Column(db.Integer,
                    nullable=False)
    
    slope = db.Column(db.Integer,
                    nullable=False)
  
class Score(db.Model):
    """Class for adding a users score"""
    
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    course_id = db.Column(db.Integer,
                        db.ForeignKey('courses.id'),
                        nullable=False)
    
    score = db.Column(db.Integer,
                      nullable=False)
    
    date = db.Column(db.Date,
                     nullable=False)