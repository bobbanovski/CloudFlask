import os
#import pdb; pdb.set_trace() #Use this to stop at a line then progress step by step.
# Press n to advance, c to continue
# print(i) to see value

from flask import Flask, request, render_template, url_for, redirect, flash, make_response
#Define instance of flask class
app = Flask(__name__) #Ensures unique application name

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
            response = make_response(redirect(url_for('welcome')))
            response.set_cookie('username', request.form.get('username'))
            return response
        else:
            error = 'incorrect username or password'
    return render_template('login.html', error=error)
    
def valid_login(username, password):
    if username == password:
        return True
    else:
        return False
        
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('username', '', expires=0) #Set the cookie's lifetime to 0
    return response
        
@app.route('/')
#def welcome(username):
def welcome():
    username = request.cookies.get('username')
    if username:
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('login'))
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.debug = True # shows full error even to outsiders
    app.secret_key = 'dsafdasgdag233d'
    app.run(host=host, port=port)