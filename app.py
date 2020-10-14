import datetime
from flask import Flask, render_template, request

# Create new Flask web application
app = Flask(__name__)

# List of user's notes
# NOTE: this is global accross the whole app
notes = []

# Webroot
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        notes.append(note)

    return render_template("index.html", notes=notes)
