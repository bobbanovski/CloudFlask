from flask_init import app #imports the __init__.py file

@app.route('/')
@app.route('/index')
def index():
    return "hello world"
