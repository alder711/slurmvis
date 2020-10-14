from flask import Flask

# Create new Flask web application
app = Flask(__name__)

# Webroot
@app.route("/")
def index():
    return "Hello, World!"

@app.route("/trevor")
def trevor():
    return "Hello, Trevor!"

@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    return f"<h1>Hello, {name}!</h1>"
