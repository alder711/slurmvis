import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session # Be able to store sessions server-side
import json
import qstatparser as qsp

# Create new Flask web application
app = Flask(__name__)
# Use the FileSystemSessionInterface session type
app.config["SESSION_TYPE"] = "filesystem"
# Don't use a permanent session
app.config["SESSION_PERMANENT"] = False
# Create the Session object, passing it the application
Session(app)



# Webroot
@app.route("/")
def index():
    json_data = qsp.parseFile("201005.1648/2.small-short-full")
    return render_template("d3-test.html", d3_dataset=json_data)


# Update Slurm qpat file
@app.route("/api/v0/fetch", methods=["GET"])
def fetchFile():
    filename = request.args.get("filename")
    json_data = None
    if filename:
        json_data = qsp.parseFile(filename) 
    return json.loads(json_data)
