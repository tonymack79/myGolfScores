
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///mygolfscores-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
      """Test users models"""
       
      def setUp(self):
          """Create test client and sample data"""
          
          db.drop_all()
          db.create_all()
          
          u1 = User.signup("test1", "test", "one", "password")
          uid1 = 1111
          u1.id = uid1

          u2 = User.signup("test2", "test", "two", "password")
          uid2 = 2222
          u2.id = uid2

          db.session.commit()

          u1 = User.query.get(uid1)
          u2 = User.query.get(uid2)

          self.u1 = u1
          self.uid1 = uid1

          self.u2 = u2
          self.uid2 = uid2

          self.client = app.test_client()
          
      def tearDown(self):
          res = super().tearDown()
          db.session.rollback()
          return res
        
      def test_user_model(self):
          """Does model work"""
          
          self.assertEqual(self.u1.username, "test1")
          self.assertEqual(self.u1.first_name, "test")
          
      def test_valid_signup(self):
          u_test = User.signup("testtesttest", "testtest", "useruser", "password")
          uid = 99999
          u_test.id = uid
          db.session.commit()

          u_test = User.query.get(uid)
          self.assertIsNotNone(u_test)
          self.assertEqual(u_test.username, "testtesttest")
          self.assertEqual(u_test.first_name, "testtest")
          self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
          self.assertTrue(u_test.password.startswith("$2b$"))

      def test_invalid_username_signup(self):
          invalid = User.signup(None, "first", "last", "password")
          uid = 123456789
          invalid.id = uid
          with self.assertRaises(exc.IntegrityError) as context:
              db.session.commit()
    
      def test_invalid_password_signup(self):
          with self.assertRaises(ValueError) as context:
              User.signup("testtest", "test", "test", "")

          with self.assertRaises(ValueError) as context:
              User.signup("testtest", "test", "test", None)
            