
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Course

os.environ['DATABASE_URL'] = "postgresql:///mygolfscores-test"

from app import app

db.create_all()

class CourseModelTestCase(TestCase):
    """Test course model"""
    
    def setUp(self):
        """Create test client, add data"""
        
        db.drop_all()
        db.create_all()
        
        c1 = Course(course_name="testcourse", par=72, slope=74, rating=120)
        cid1 = 1111
        c1.id = cid1
        
        db.session.add(c1)
        db.session.commit()
        
        c1 = Course.query.get(cid1)
        
        self.c1 = c1
        self.cid1 = cid1
        
        self.client = app.test_client()
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
      
    def test_course_model(self):
        """Test basic course model"""
        
        self.assertEqual(self.c1.course_name, "testcourse")
        self.assertEqual(self.c1.par, 72)