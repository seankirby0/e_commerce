from app import app
from flask import render_template


@app.route('/')
def home_page():
    return "Welcome to The Shop"

