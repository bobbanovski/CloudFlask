import os

from flask import Flask
#Define instance of flask class
app = Flask(__name__) #Ensures unique application name

@app.route('/')
def indexPage():
    return 'Welcome to CloudFlask'
    
@app.route('/users/<username>')
def usersPage(username):
    visits = 3
    return "Personal page of: %s, you have visited %d times" % (username, visits)
    
@app.route('/posts/<int:post_id>') #if not an int, 404 not found is shown
def posts(post_id):
    return 'Post with id: %d' % post_id


@app.route('/hello') #return function helloWorld to person who accesses /
def helloWorld():
    i = 3
    #import pdb; pdb.set_trace() #Use this to stop at a line then progress step by step.
    # Press n to advance, c to continue
    # print(i) to see value
    i+=1
    return 'Good Morning!' + " You've visited " + str(i) + ' times'
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.debug = True # shows full error even to outsiders
    app.run(host=host, port=port)