from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
@app.route("/")
def main(): 
    return render_template("index.html")


@app.route("/discussion")
def discussion(): 
    return "Discussion page"

@app.route("/events")
def events(): 
    return "Events page"

@app.route("/about")
def about(): 
    return "About page" 
def create_app():
    return app





