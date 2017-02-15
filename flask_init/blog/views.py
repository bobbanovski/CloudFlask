from flask_init import app #imports the __init__.py file
from flask import render_template, flash, redirect, url_for
from blog.form import SetupForm
from flask_init import db
from author.models import Author
from blog.models import Blog

@app.route('/')
@app.route('/index')
def index():
    return "hello world"

@app.route('/admin')
def admin():
    blogs = Blog.query.count()
    if blogs == 0:
        return redirect(url_for('setup'))
    return render_template('/blog/admin.html')
    
@app.route('/setup', methods=('GET', 'POST'))
def setup():
    form = SetupForm()
    error = ""
    if form.validate_on_submit():
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            form.password.data,
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