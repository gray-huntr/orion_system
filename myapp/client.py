from myapp import myapp
import pymysql
from flask import render_template, url_for


# Route to serve the static files, i.e css
@myapp.route('/static/<path:filename>')
def serve_static(filename):
    # Assuming 'your_package' is your package name
    return myapp.send_static_file(f'myapp/{filename}')


# Route for the index page
@myapp.route("/")
def home():
    conn = initiate
    return render_template("patients/index.html")


# Route for the login page
@myapp.route("/login")
def login():
    return render_template("patients/login.html")


# Route for the patient page
@myapp.route("/patient")
def patient():
    return render_template("patients/patient.html")


# Route for the signup page
@myapp.route("/signup")
def signup():
    return render_template("patients/signup.html")
