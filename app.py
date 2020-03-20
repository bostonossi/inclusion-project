from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/intake")
def intake():
    return render_template('intake.html')