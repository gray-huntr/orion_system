from myapp import myapp as app
from flask import render_template, url_for, request, redirect, flash, session
import pymysql

app.secret_key = app.config['SECRET_KEY']


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
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        cursor.execute("select * from patients where email = %s and password = %s", (email, password))
        if cursor.rowcount == 0:
            flash("Incorrect username or password, try again", "warning")
            return redirect("/login")
        elif cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                session['patientId'] = row[0]
                if row[7] == 1:
                    flash("Please set a new password before continuing", "info")
                    return redirect("/password_change")
                else:
                    return redirect("/patient")
        else:
            flash("Error occurred", "danger")
            return redirect("/login")
    else:
        if 'staffId' in session:
            session.pop('staffId', None)
            return redirect('/login')
        else:
            return render_template("patients/login.html")

# Route for the signup page
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        repeat_pass = request.form['repeatPass']

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

# Route for the patient page
@app.route("/patient")
def patient():
    return render_template("patients/patient.html")


@app.route("/appointments/<action>", methods=['POST', 'GET'])
def appointments(action):
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if action == 'view':
        if request.method == 'POST':
            time = request.form['time']

            cursor.execute("insert into appointments(patientId, time) VALUES (%s,%s)",
                           (session['patientId'], time))
            conn.commit()
            flash("Appointment booked successfully", "success")
            return redirect("/appointments")
        else:
            cursor.execute("select * from appointments")
            if cursor.rowcount == 0:
                flash("You haven't made any appointments yet", "info")
                return render_template("patients/appointments.html")
            elif cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("patients/appointments.html", rows=rows)
    elif action == 'cancel':
        id = request.form['id']

        cursor.execute("update appointments set status = 'Cancelled' where appointmentId = %s", id)
        conn.commit()
        return redirect("/appointments/view")

@app.route("/logout")
def logout():
    if 'patientId' in session:
        session.pop('patientId', None)
        return redirect("/login")
    if 'staffId' in session:
        session.pop('staffId', None)
        return redirect("/staff_login")