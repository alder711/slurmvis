import datetime
from flask import Flask, render_template, request, session
from flask_session import Session # Be able to store sessions server-side

# Create new Flask web application
app = Flask(__name__)
# Use the FileSystemSessionInterface session type
app.config["SESSION_TYPE"] = "filesystem"
# Don't use a permanent session
app.config["SESSION_PERMANENT"] = False
# Create the Session object, passing it the application
Session(app)



# Webroot
@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:
        session["notes"] = []
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)

    return render_template("index.html", notes=session["notes"])
