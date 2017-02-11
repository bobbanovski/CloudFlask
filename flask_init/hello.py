import os
import pymysql
import logging
#import pdb; pdb.set_trace() #Use this to stop at a line then progress step by step.
# Press n to advance, c to continue
# print(i) to see value

from flask import Flask, request, render_template, url_for, redirect, flash, session
#Define instance of flask class
app = Flask(__name__) #Ensures unique application name
from logging.handlers import RotatingFileHandler #prevents filling of space on server

@app.route('/users/<username>')
def usersPage(username):
    visits = 3
    return "Personal page of: %s, you have visited %d times" % (username, visits)
    
@app.route('/posts/<int:post_id>') #if not an int, 404 not found is shown
def posts(post_id):
    return 'Post with id: %d' % post_id

@app.route('/hello')
@app.route('/hello/<name>') #return function helloWorld to person who accesses /
def hello(name=None): # None = not required
    return render_template('hello.html', name_t = name)
    
@app.route('/login', methods=['GET', 'POST']) #Form submitted with GET method
def login():
    error = None
    if request.method == 'POST':
        if (valid_login(request.form['username'], request.form['password'])): # %d already assigned to int
            flash("successfully logged in") #Stores on the session cookie, resets after retrieval
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'incorrect username or password'
            app.logger.warning('incorrect username or password for user: %s',
                request.form.get('username')) #can set levels of log eg warning
    return render_template('login.html', error=error)
    
def valid_login(username, password):
    #SQL query
    MYSQL_DATABASE_HOST = os.getenv('IP', '0,0,0,0')
    MYSQL_DATABASE_USER = 'bobbanovski'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'cloudflaskdb'
    conn = pymysql.connect(
        host = MYSQL_DATABASE_HOST,
        user = MYSQL_DATABASE_USER,
        passwd = MYSQL_DATABASE_PASSWORD,
        db = MYSQL_DATABASE_DB
        )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='%s' AND password='%s'" %
        (username, password))
    data = cursor.fetchone()
    
    if data:
        return True
    else:
        return False
        
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
        
@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.debug = True # shows full error even to outsiders
    app.secret_key = 's\xce\xabB|\x10\xae\x0c\x87\xe2\xff(2(\xa8\x1a_\x8a\x16r\xa81\xc3\n'
    #enable logging, save to error.log, maximum size of 10MB
    handler = RotatingFileHandler('error.log', maxBytes=10000000, backupCount = 1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host=host, port=port)