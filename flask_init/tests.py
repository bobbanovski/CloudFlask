# set the path like with __init__.py
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flast.ext.sqlalchemy import SQLAlchemy

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
        self.db_uri = "mysql+pymysql://%s:%s@%s" % (db_username, db_password, db_host)
        
        #settings for testing
        app.config['TESTING'] = True #flag for testing mode in Flask
        app.config['WTF_CSRF_ENABLED'] = False #Turn of CSRF protection to allow http calls
        app.config['BLOG_DATABASE_NAME'] = 'test-cloudflaskdb'
        app.conifg['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        
        #create sqlalchemy instance for engine
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        
        conn.execute('commit')
        conn.execute('CREATE DATABASE' + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        
        self.app = app.test_client()