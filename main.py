import os 
from flask import Flask, get_flashed_messages, flash, render_template, request, url_for, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

##database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'super-secret-key'

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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    author = db.Column(db.String)
    link = db.Column(db.String)
    kind = db.Column(db.String)

    def __init__(self, title, description, author, link, kind):
        self.title = title
        self.description = description
        self.author = author
        self.link = link
        self.kind = kind

    def __repr__(self):
        return f'<Post title: {self.title}>'
    

class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)  # Make sure to hash passwords in a real app
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    def __init__(self, username, password, event_id):
        self.username = username
        self.password = password  # In production, hash the password
        self.event_id = event_id

    def __repr__(self):
        return f'<SignUp {self.username} for Event ID: {self.event_id}>'

    

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True)
    password=db.Column(db.String, nullable=False)

    def __init__(self, user, pw):
        self.username = user
        self.password = pw 

    def __repr__(self):
        return f'Username: {self.username}'


with app.app_context(): 
    db.create_all()


#App routing
@app.route("/", methods=['GET', 'POST'])
def main(): 
    error = None
    get_flashed_messages()
    if request.method== 'POST': 

        username=request.form.get('username')
        password=request.form.get('password')
        user = User.query.filter_by(username=username).first() #check if user exists

        if not user or not (user.password==password):
            flash("Try again dummy")
            print("wrong")
            return redirect(url_for('main'))
        return redirect(url_for('discussion'))

    return render_template('index.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup(): 
    if request.method=='POST':
        username=request.form.get("username")
        password=request.form.get("password")

        user = User.query.filter_by(username=username).first() #check if there is already a user with that username

        if user: #maybe add an error message for this ?
            flash("Email address already exists, try again")
            #return redirect(url_for('signup')) #return to signup page if user already exists
        else: 
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('main'))     


    return render_template('signup.html')


@app.route('/logout')
def logout(): 
    return 'Logout'


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
        

@app.route("/events", methods=['GET', 'POST'])
def events(): 
    all_events = Event.query.all()
    if request.method == 'POST': 
        title = request.form.get("title")
        description = request.form.get("description")
        link = request.form.get("link")
        author = request.form.get("author")  # Assuming you want to capture the author's name
        kind = request.form.get("kind")
        
        if kind == 'Other':
            kind = request.form.get("other")
        
        new_event = Event(title=title, description=description, author=author, link=link, kind=kind)
        db.session.add(new_event)  # Create new event in Event database
        db.session.commit()
        all_events = Event.query.all()  # Fetch updated events
        print(all_events)
        return render_template("events.html", allEvents=all_events, testVar="Test!!")
    return render_template("events.html", allEvents=all_events, testVar="Test!!")

@app.route('/volunteer/<event_title>', methods=['GET'])
def volunteer(event_title):
    print(f"Requested signup for event: {event_title}")  # Debugging line
    event = Event.query.filter_by(title=event_title).first()  # Fetch the specific event by title
    if event:
        return render_template('volunteer.html', event_title=event.title, event_id=event.id)
    print("Event not found.")  # Debugging line
    return redirect(url_for('events'))  # Redirect if event not found

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    username = request.form.get('username')
    password = request.form.get('password')  # In production, hash this password
    event_id = request.form.get('event_id')

    # Create a new sign-up entry
    signup = SignUp(username=username, password=password, event_id=event_id)
    
    
    db.session.add(signup)
    db.session.commit()

    # Redirect to a success page or back to events
    return redirect(url_for('events'))  # You can change this to a success page if needed


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
    


