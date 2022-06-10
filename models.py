from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

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
    # May have to change password for wtforms-alchemy
    password = db.Column(db.Text,
                         nullable=False)
    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"
      
    @classmethod
    def signup(cls, username, first_name, last_name, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
      
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

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
    
    date = db.Column(db.DateTime,
                     nullable=False)
    
    @property
    def friendly_date(self):
        """Return nicely formatted date"""
        return self.date.strftime("%B %-d, %Y")