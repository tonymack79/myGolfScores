
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Course, Score

os.environ['DATABASE_URL'] = "postgresql:///mygolfscores-test"

from app import app

db.create_all()

class ScoreModelTestCase(TestCase):
    """Tests score model"""
    
    def setUp(self):
        """Create test client and add data"""
        
        db.drop_all()
        db.create_all()
        
        u = User(username="test", first_name="test", last_name="user", password="password")
        uid = 123
        u.id = uid
        
        c = Course(course_name="test course", par=72, slope=74, rating=120)
        cid = 111
        c.id = cid
        
        db.session.add(u)
        db.session.add(c)
        db.session.commit()
        
        u = User.query.get(uid)
        c = Course.query.get(cid)
        
        self.u = u
        self.c = c
        
        self.client = app.test_client()
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
      
    def test_score_model(self):
        """Does basic model work"""
        
        s = Score(user_id=self.u.id, course_id=self.c.id, score=80)
        sid = 12
        s.id = sid
        
        db.session.add(s)
        db.session.commit()
        
        s = Score.query.get(sid)
        
        self.s = s
        
        self.assertEqual(self.s.score, 80)
        
        