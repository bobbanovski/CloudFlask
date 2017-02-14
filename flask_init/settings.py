import os

SECRET_KEY = 's\xce\xabB|\x10\xae\x0c\x87\xe2\xff(2(\xa8\x1a_\x8a\x16r\xa81\xc3\n'
DEBUG = True

DB_USERNAME = 'bobbanovski'
DB_PASSWORD = ''
DB_NAME = 'cloudflaskdb'
DB_HOST = os.getenv('IP', '0,0,0,0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI #cannot change sqlalchemy variable name
SQLALCHEMY_TRACK_MODIFICATIONS = True
