from flask_init import app #imports the __init__.py file
from flask import render_template, flash, redirect, url_for, session, abort
from blog.form import SetupForm, PostForm
from flask_init import db
from author.models import Author
from blog.models import Blog, Category, Post
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify

@app.route('/')
@app.route('/index')
def index():
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    posts = Post.query.order_by(Post.publishDate.desc())
    
    return render_template('/blog/index.html', posts = posts, blog=blog)

@app.route('/admin')
@author_required
def admin():
    if session.get('is_author'):
        posts = Post.query.order_by(Post.publishDate.desc())
        return render_template('/blog/admin.html', posts = posts)
    else:
        abort(403)
        
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
    
@app.route('/post', methods=('GET', 'POST'))
@author_required
def post():
    form=PostForm()
    if form.validate_on_submit():
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category=new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data) #get primary key of Category
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None
        blog = Blog.query.first() #change later to pick out specific blog
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        
        post = Post(blog, author, category, title, body, slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
    return render_template('blog/post.html', form=form)
    
@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
        
    return render_template('blog/article.html', post = post)
