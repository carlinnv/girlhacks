from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

##database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"

db.init_app(app)



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