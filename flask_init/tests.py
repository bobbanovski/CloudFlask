# set the path like with __init__.py
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask_init import app,db

#models
from author.models import *
from blog.models import *

class userTest(unittest.TestCase):
    def setUp(self): #called at start of test - temp database created
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        db_name = app.config['DB_NAME']
        self.db_uri = "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
        
        #settings for testing
        app.config['TESTING'] = True #flag for testing mode in Flask
        app.config['WTF_CSRF_ENABLED'] = False #Turn of CSRF protection to allow http calls
        app.config['BLOG_DATABASE_NAME'] = 'test_cloudflaskdb'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        
        #create sqlalchemy instance for engine
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        
        conn.execute('commit')
        conn.execute("CREATE DATABASE " + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        
        self.app = app.test_client()
        
    def tearDown(self): # takes down test database after test
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute("DROP DATABASE " + app.config['BLOG_DATABASE_NAME'])
        conn.close()
        
    #test for create blog
    def create_blog(self):
        return self.app.post('/setup', data=dict(
            name="A Test Blog",
            fullname="Robert C",
            email = "demo@demo.com",
            username = "bobbanovski",
            password = "muhPassword",
            confirm = "muhPassword"
            ),
            follow_redirects=True)
            
    def test_create_blog(self): #must always start with test_ to run automatically
        rv = self.create_blog()
        #print(rv.data)
        assert 'blog created' in str(rv.data)
    
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ),
            follow_redirects = True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def test_login_logout(self):
        self.create_blog()
        rv = self.login('bobbanovski','muhPassword')
        assert 'user bobbanovski logged in' in str(rv.data)
        rv = self.logout()
        assert 'user logged out' in str(rv.data)
        
        rv = self.login('bobbanovski','completelyWrong')
        assert 'Login unsuccessful' in str(rv.data)
        rv = self.login('wrongname', 'muhPassword')
        assert 'Login unsuccessful' in str(rv.data)
        
if __name__ == '__main__':
    unittest.main()