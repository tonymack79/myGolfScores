import os
from unittest import TestCase
from sqlalchemy import exc
from flask import session
from models import db, connect_db, User, Course, Score

os.environ['DATABASE_URL'] = "postgresql:///mygolfscores-test"

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for users"""
    
    def setUp(self):
        """Create test client"""
        app.config['LOGIN_DISABLED'] = True
        
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()
        
        u = User(username="test1", first_name="test", last_name="one", password="password")
        uid = 1111
        u.id = uid
        
        c = Course(course_name="test course", par=72)
        cid = 1212
        c.id = cid
        
        s = Score(user_id=u.id, course_id=c.id, score=72, date='2022-06-19 00:00:00')
        sid = 1234
        s.id = sid
        
        db.session.add(u)
        db.session.add(c)
        db.session.add(s)
        db.session.commit()
        
        u = User.query.get(uid)
        c = Course.query.get(cid)
        s = Score.query.get(sid)
        
        self.u = u
        self.c = c
        self.s = s
        
        self.client = app.test_client()
        
        # with self.client as c:
        #     resp = c.get('/login')
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
      
    def test_homepage(self):
        """Test home page"""
        with self.client as c:
            with c.session_transaction() as change_session:
                change_session['_user_id'] = self.u.id
                
            resp = c.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a>test course</a>', html)
      
    def test_select_course(self):
        with self.client as c:
            resp = c.get('/course', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a>test course</a>', html)
      
    def test_add_course(self):
        with self.client as c:
            resp = c.get('/course/add', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="h4 mb-4">Add a new course</p>', html)
            
    def test_add_score(self):
        with self.client as c:
            with c.session_transaction() as change_session:
                change_session['_user_id'] = self.u.id
                
            resp = c.get(f'/course/{self.c.id}/score/add', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="h4 mb-4">Add Score</p>', html)
      