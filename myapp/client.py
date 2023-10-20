from myapp import myapp, server
from flask import render_template, url_for, request, redirect

cursor = server.connect()


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
        email = request.form['email']
        password = request.form['password']

        if server.authenticate(cursor, email, password):
            return redirect('/')
        else:
            return "Wrong Username or password"
    else:
        pass
    return render_template("patients/login.html")


# Route for the patient page
@myapp.route("/patient")
def patient():
    return render_template("patients/patient.html")


# Route for the signup page
@myapp.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        repeat_pass = request.form['repeatPass']

        if repeat_pass != password:
            return ("Passwords Do not Match")
        
        if server.signup(cursor=cursor, fullname=fullname, email=email, password=password):
            return redirect('/')
        else:
            return redirect('/signup')
            
        
        
    return render_template("patients/signup.html")
