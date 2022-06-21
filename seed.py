from app import app
from models import db, User, Course, Score

db.drop_all()
db.create_all()

edgewood = Course(course_name='Edgewood', par=71)
prairewood = Course(course_name='Prairewood', par=32)
el_zagel = Course(course_name='El Zagel', par=27)
rose_creek = Course(course_name='Rose Creek', par=71)
osgood = Course(course_name='Osgood', par=33)

db.session.add(edgewood)
db.session.add(prairewood)
db.session.add(el_zagel)
db.session.add(rose_creek)
db.session.add(osgood)

db.session.commit()