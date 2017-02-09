import os
#import pdb; pdb.set_trace() #Use this to stop at a line then progress step by step.
# Press n to advance, c to continue
# print(i) to see value

from flask import Flask, request, render_template
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
    if request.method == 'POST':
        return 'username entered was: %s' % request.values["username"] # %d already assigned to int
    return '<form method="post" action="/login"><input type="text" name="username" /><br/><button type=submit>Submit</button></form>'
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.debug = True # shows full error even to outsiders
    app.run(host=host, port=port)