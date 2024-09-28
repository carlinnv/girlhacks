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
    db.session.add(Post('Test', 'caption'))

    posts = Post.query.all()
    print(posts) 


#App routing
@app.route("/")
def main(): 
    
    return "<p>test main</p>"


@app.route("/discussion", methods=['GET'])
def discussion(): 
    if request.method == 'GET': 
        return render_template("discussion.html")
        


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
    app.run()