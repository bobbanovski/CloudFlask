from flask_init import app
from flask import render_template, redirect, url_for, session, request
from author.form import RegisterForm, LoginForm
from flask_init import db
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = ""
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')
        
    if form.validate_on_submit():
        authors = Author.query.filter_by(
            username = form.username.data
            ).limit(1)
        if authors.count():
            author = authors[0]
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('loginSuccess'))
            else:
                error = "Login unsuccessful"
        else:
            error = "Login unsuccessful"
    return render_template('author/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('registersuccess'))
    return render_template('author/register.html', form=form)
    
@app.route('/registersuccess')
def registersuccess():
    return "Author registered successfully"
    
@app.route('/loginSuccess')
@login_required
def loginSuccess():
    return "Logged in successfully"
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))