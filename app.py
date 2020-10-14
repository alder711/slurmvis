import datetime
from flask import Flask, render_template, request

# Create new Flask web application
app = Flask(__name__)

# Webroot
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return "Please submit the form instead."
    else:
        name = request.form.get("name")
        return render_template("hello.html", name=name)
