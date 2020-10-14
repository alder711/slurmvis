import datetime
from flask import Flask, render_template

# Create new Flask web application
app = Flask(__name__)

# Webroot
@app.route("/")
def index():
    names = ["Alice", "Bob", "Charlie"]
    return render_template("index.html", names=names)
