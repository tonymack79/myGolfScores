from app import db
from models import User, Course, Score

db.drop_all()
db.create_all()

db.session.commit()