from myapp import myapp, sql_db
from flask import render_template, url_for, request, redirect

cursor = sql_db.establish_connection()


# Route to serve the static files, i.e css
@myapp.route('/static/<path:filename>')
def serve_static(filename):
    # Assuming 'your_package' is your package name
    return myapp.send_static_file(f'myapp/{filename}')


# Route for the index page
@myapp.route("/")
def home():
    return render_template("patients/index.html")


# Route for the login page
@myapp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        if sql_db.authenticate(cursor, username, password) < 1:
            return "Wrong Username or password"
        else:
            return redirect('/')
    else:
        pass
    return render_template("patients/login.html")


# Route for the patient page
@myapp.route("/patient")
def patient():
    return render_template("patients/patient.html")


# Route for the signup page
@myapp.route("/signup")
def signup():
    return render_template("patients/signup.html")
