from flask_init import db
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        
    def __repr__(self):
        return '<blog %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    blogId = db.Column(db.Integer, db.ForeignKey('blog.id'))
    authorId = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(50))
    body = db.Column(db.Text)
    slug = db.Column(db.String(256), unique=True)
    publishDate = db.Column(db.DateTime)
    live = db.Column(db.Boolean) #Instead of deleting, mark as false
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    def __init__(self, blog, author, title, body, slug=None, publishDate=None, live=True):
        self.blogId=blog.id
        self.authorId=author.id
        self.title=title
        self.body=body
        self.slug=slug
        if publishDate is None:
            self.publishDate=datetime.utcnow()
        else:
            self.publishDate=publishDate
        self.live=live
        
    def __repr__(self):
        return '<post %r>' % self.title
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __init__(self,name):
        self.name=name
        
    def __repr__(self):
        return '<category %r>' % self.name