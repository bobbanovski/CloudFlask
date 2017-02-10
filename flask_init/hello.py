import os
#import pdb; pdb.set_trace() #Use this to stop at a line then progress step by step.
# Press n to advance, c to continue
# print(i) to see value

from flask import Flask, request, render_template, url_for, redirect
#Define instance of flask class
app = Flask(__name__) #Ensures unique application name

@app.route('/')
def indexPage():
    return 'Welcome to CloudFlask'
    #return url_for('usersPage', username='Robert') #need to import url_for
    
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
            return redirect(url_for('welcome', username=request.form.get('username')))
        else:
            error = 'incorrect username or password'
    return render_template('login.html', error=error)
    
def valid_login(username, password):
    if username == password:
        return True
    else:
        return False
        
@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.debug = True # shows full error even to outsiders
    app.run(host=host, port=port)