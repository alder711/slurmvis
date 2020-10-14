from flask import Flask, render_template

# Create new Flask web application
app = Flask(__name__)

# Webroot
@app.route("/")
def index():
    headline = "Hello!"
    return render_template("index.html", headline=headline)
