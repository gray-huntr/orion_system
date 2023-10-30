from myapp import myapp as app
from flask import render_template, url_for, request, redirect, flash
import pymysql
app.secret_key = app.config['SECRET_KEY']

# connect to database
conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                       password=app.config["DB_PASSWORD"],
                       database=app.config["DB_NAME"])

# Route to serve the static files, i.e css
@app.route('/static/<path:filename>')
def serve_static(filename):
    # Assuming 'your_package' is your package name
    return app.send_static_file(f'app/{filename}')


# Route for the index page
@app.route("/")
def home():
    return render_template("patients/index.html")


# Route for the login page
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("select * from patients where email = %s and password = %s",(email,password))
        if cursor.rowcount == 0:
            flash("Incorrect username or password, try again", "warning")
            return redirect("/login")
        elif cursor.rowcount == 1:
            return redirect("/")
        else:
            flash("Error occurred", "danger")
            return redirect("/login")
    else:
        return render_template("patients/login.html")


# Route for the patient page
@app.route("/patient")
def patient():
    return render_template("patients/patient.html")


# Route for the signup page
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        repeat_pass = request.form['repeatPass']

        cursor = conn.cursor()
        cursor.execute("select * from patients where email = %s", email)
        if cursor.rowcount > 0:
            flash("Email already exists, try another one", "info")
            return redirect("/signup")
        elif cursor.rowcount == 0:
            if password == repeat_pass:
                cursor.execute("insert into patients(fullname, email, number, password) values (%s,%s,%s,%s)",
                               (fullname, email, number, password))
                conn.commit()
                flash("Sign up successfull", "success")
                return redirect("/signup")
            elif password != repeat_pass:
                flash("Passwords do not match", "danger")
                return redirect("/signup")
        else:
            flash("Error occured", "danger")
            return redirect("/signup")
    else:
        return render_template("patients/signup.html")
