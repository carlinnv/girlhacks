import os 
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

##database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"

db.init_app(app)

##create database for discussion posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    caption = db.Column(db.String)

    def __init__(self, title, caption):
        self.title = title
        self.caption = caption

    def __repr__(self):
        return f'<Post title: {self.title}>'
    

with app.app_context(): 
    db.create_all()


#App routing
@app.route("/")
def main(): 
    return render_template("index.html")


@app.route("/discussion", methods=['GET', 'POST'])
def discussion(): 
    posts = Post.query.all()
    if request.method == 'POST': 
        title = request.form.get("title")
        caption = request.form.get("caption")
        db.session.add(Post(title, caption)) #create new post in Post database
        db.session.commit()
        posts = Post.query.all()
        print(posts)
        return render_template("discussion.html", allPosts = posts, testVar = "Test!!")
    return render_template("discussion.html", allPosts = posts, testVar = "Test!!")
        


@app.route("/events")
def events(): 
    return "Events page"

@app.route("/about")
def about(): 
    return "About page" 



@app.route("/testing")
def testing(): 
    return "Can Forum see this..."

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    debug = True
    app.run()
    