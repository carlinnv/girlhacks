from flask import Flask
app = Flask(__name__)

@app.route("/")
def main(): 
    return "<p>test main</p>"


@app.route("/discussion")
def discussion(): 
    return "Discussion page"

@app.route("/events")
def events(): 
    return "Events page"

@app.route("/about")
def about(): 
    return "About page" 



@app.route("/testing")
def testing(): 
    return "Can Forum see this..."