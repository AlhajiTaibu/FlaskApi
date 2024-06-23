from flask import Flask, render_template, url_for, redirect, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to Flask"
