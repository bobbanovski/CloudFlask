from flask_init import app
from flask import render_template, redirect, url_for, session, request, flash
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
        author = Author.query.filter_by(
            username = form.username.data
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                flash('user ' + form.username.data + " logged in")
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
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
    
@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    flash('user logged out')
    return redirect(url_for('index'))