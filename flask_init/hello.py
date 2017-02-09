import os

from flask import Flask
#Define instance of flask class
app = Flask(__name__) #Ensures unique application name

@app.route('/') #return function helloWorld to person who accesses /
def helloWorld():
    return 'Good Morning!'
    
#called from terminal, command line
if __name__ == '__main__': 
    host = os.getenv('IP', '0.0.0.0')  # Get the host
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port)