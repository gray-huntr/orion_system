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
                if row[10] == 1:
                    flash("Please set a new password before continuing", "info")
                    return redirect("/password_change_patient")
                else:
                    return redirect("/patient")
        else:
            flash("Error occurred", "danger")
            return redirect("/login")
    else:
        return render_template("patients/index.html")


# Route for the patient page
@app.route("/patient")
def patient():
    if 'patientId' in session:
        return render_template("patients/appointments.html")
    else:
        flash("Please login first", "info")
        return redirect("/login")


@app.route("/appointments/<action>", methods=['POST', 'GET'])
def appointments(action):
    if 'patientId' in session:
        # connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        if action == 'view':
            if request.method == 'POST':
                with open("myapp/db_ids/appointment_id", "r") as file:
                    old_id = int(file.read())
                    appointment_id = "A" + str(old_id)
                time = request.form['time']

                cursor.execute("insert into appointments(appointmentId, patientId, time, category) VALUES (%s, %s,%s,%s)",
                               (appointment_id, session['patientId'], time, 'online'))
                conn.commit()
                old_id += 1
                # Save the new appointment id to file
                with open("myapp/db_ids/appointment_id", "w") as file:
                    file.write(str(old_id))
                flash("Appointment booked successfully,", "success")
                return redirect("/appointments/view")
            else:
                cursor.execute("select * from appointments where patientId = %s", session['patientId'])
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
    else:
        flash("Please login first", "info")
        return redirect("/login")


@app.route("/my_billings")
def my_billings():
    if 'patientId' in session:
        # connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from billing where patientId = %s", session['patientId'])
        if cursor.rowcount == 0:
            flash("There are no billing records for you", "info")
            return render_template("patients/billing.html")
        elif cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("patients/billing.html", rows=rows)
    else:
        flash("Please login first", "info")
        return redirect("/login")


@app.route("/treatment_report")
def treatment_report():
    if 'patientId' in session:
        # connect to database
        conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                               password=app.config["DB_PASSWORD"],
                               database=app.config["DB_NAME"])
        cursor = conn.cursor()
        cursor.execute("select * from treatment where patientId = %s", session['patientId'])
        if cursor.rowcount == 0:
            flash("You dont have any treatment records", "info")
            return render_template("patients/treatment_report.html")
        elif cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("patients/treatment_report.html", rows=rows)
    else:
        flash("Please login first", "info")
        return redirect("/login")


@app.route("/logout_patient")
def logout_patient():
    session.pop('patientId', None)
    return redirect("/login")
