from flask_init import app #imports the __init__.py file
from flask import render_template, flash, redirect, url_for
from blog.form import SetupForm
from flask_init import db
from author.models import Author
from blog.models import Blog
from author.decorators import login_required
import bcrypt

@app.route('/')
@app.route('/index')
def index():
    blogs = Blog.query.count()
    if blogs == 0:
        return redirect(url_for('setup'))
    return "hello world"

@app.route('/admin')
@login_required
def admin():
    return render_template('/blog/admin.html')
    
@app.route('/setup', methods=('GET', 'POST'))
def setup():
    form = SetupForm()
    error = ""
    if form.validate_on_submit():
        salt = bcrypt.gensalt() #generate password salt
        hashedPassword = bcrypt.hashpw(form.password.data, salt) 
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashedPassword,
            True
            )
        db.session.add(author)
        db.session.flush() #sqlalchemy simulates writing the record, checks validation
        if author.id:
            blog = Blog(
                form.name.data,
                author.id
                )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "error in creating user"
        if author.id and blog.id:
            db.session.commit()
            flash("blog created")
            return redirect(url_for('admin'))
        else:
            db.session.rollback()
            error = "error in creating blog"
    
    return render_template('blog/setup.html', form=form, error=error)