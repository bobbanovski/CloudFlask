from flask_init import app

@app.route('/login')
def login():
    return 'hello author'
