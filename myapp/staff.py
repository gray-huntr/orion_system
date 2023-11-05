from myapp import myapp as app
from flask import render_template, request, flash, redirect, session
import pymysql


@app.route("/staff_login", methods=['POST', 'GET'])
def staff_login():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("select * from staff where email = %s and password = %s", (email, password))
        if cursor.rowcount == 0:
            flash("Incorrect username or password, try again", "warning")
            return redirect("/staff_login")
        elif cursor.rowcount == 1:
            rows = cursor.fetchall()
            for row in rows:
                category = row[5]
                session['staffId'] = row[0]
                if row[6] == 1:
                    flash("Please set a new password before continuing", "info")
                    return redirect("/password_change")
                else:
                    if category == "Doctor":
                        return redirect("/doctor")
                    elif category == "Receptionist":
                        return redirect("/reception")
                    elif category == "Cashier":
                        return render_template("staff/cashier/cashier.html")
                    else:
                        flash("Error occurred", "warning")
                        return redirect("/staff_login")
        else:
            flash("Error occurred", "danger")
            return redirect("/staff_login")
    else:
        if 'patientId' in session:
            session.pop('patientId', None)
            return redirect("/staff_login")
        else:
            return render_template("staff/staff_login.html")


@app.route("/password_change", methods=['POST', 'GET'])
def password_change():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        repeat_password = request.form['repeat_password']

        if 'staffId' in session:
            cursor.execute("select * from staff where staffId = %s and password = %s",
                           (session['staffId'], old_password))
            if cursor.rowcount == 0:
                flash("Your old password is incorrect", "danger")
                return redirect("/password_change")
            elif cursor.rowcount == 1:
                if new_password == repeat_password:
                    cursor.execute("update staff set firstLogin = '0', password = %s where staffId = %s",
                                   (new_password, session['staffId']))
                    conn.commit()
                    flash("Password changed successfully, login to continue", "success")
                    return redirect("/staff_login")
                else:
                    flash("New passwords do not match", "danger")
                    return redirect("/password_change")
        if 'patientId' in session:
            cursor.execute("select * from patients where patientId = %s and password = %s",
                           (session['patientId'], old_password))
            if cursor.rowcount == 0:
                flash("Your old password is incorrect", "danger")
                return redirect("/password_change")
            elif cursor.rowcount == 1:
                if new_password == repeat_password:
                    cursor.execute("update patients set firstLogin = '0', password = %s where patientId = %s",
                                   (new_password, session['patientId']))
                    conn.commit()
                    flash("Password changed successfully", "success")
                    return redirect("/")
                else:
                    flash("New passwords do not match", "danger")
                    return redirect("/password_change")
    else:
        return render_template("password_change.html ")


#     Routes for receptionists
@app.route("/reception")
def reception():
    return render_template("staff/reception/receptionist.html")


@app.route("/register_patient", methods=['POST', 'GET'])
def register_patient():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        dob = request.form['dob']
        number = request.form['number']
        id_number = request.form['id_number']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        password = "Patient@orion"

        cursor.execute("select * from patients where email = %s", email)
        if cursor.rowcount > 0:
            flash("The email has already been registered, use another one", "warning")
            return redirect("/register_patient")
        elif cursor.rowcount == 0:
            cursor.execute(
                "insert into patients(fullname, email, number, id_number, password, gender, DOB, blood_group)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (fullname, email, number, id_number, password, gender, dob, blood_group))
            conn.commit()
            flash("Patient registered successfully", "success")
            return redirect("/register_patient")
    else:
        return render_template("staff/reception/register_patient.html")


@app.route("/appointment_search", methods=['POST', 'GET'])
def appointment_search():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['id']

        cursor.execute("select appointments.*, patients.* from appointments "
                       "inner join patients on appointments.patientId = patients.patientId "
                       "where appointments.category = 'online' and (patients.patientId = %s or patients.fullname like %s "
                       "or appointments.appointmentId = %s) ",
                       (id, '%' + id + '%', id))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("staff/reception/appointments.html", rows=rows)
        elif cursor.rowcount == 0:
            flash(f"There is no appointment with the search term: {id}", "info")
            return redirect("/appointment_search")
    else:
        return render_template("staff/reception/appointments.html")


@app.route("/assign_room/<category>/<id>", methods=['POST', 'GET'])
def assign_room(category, id):
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if category == 'online':
        if request.method == 'POST':
            room = request.form['room']

            cursor.execute("update appointments set roomNo = %s where appointmentId = %s", (room, id))
            conn.commit()
            flash("Room assigned successfully", "success")
            return redirect("/appointment_search")
        else:
            flash("Error occurred, please try again", "danger")
            return redirect("/appointment_search")
    elif category == 'walk-in':
        if request.method == 'POST':
            # read the appointment id
            with open("myapp/db_ids/appointment_id", "r") as file:
                old_id = int(file.read())
                appointment_id = "A" + str(old_id)
            room = request.form['room']
            patient_id = id
            status = "attending"
            category = "walk-in"

            cursor.execute("insert into appointments(appointmentId, patientId, roomNo, status, category) "
                           "values (%s,%s,%s,%s,%s)", (appointment_id, patient_id, room, status, category))
            conn.commit()
            old_id += 1
            # Save the new appointment id to file
            with open("myapp/db_ids/appointment_id", "w") as file:
                file.write(str(old_id))
            flash("Room assigned successfully", "success")
            return redirect("/walkins")


@app.route("/walkins", methods=['POST', 'GET'])
def walkins():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['id']

        cursor.execute("select * from patients where patientId = %s or fullname like %s",
                       (id, '%' + id + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("staff/reception/walk-ins.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("Their id no patient with the given id or name, try again", "warning")
            return redirect("/walkins")
    else:
        return render_template("staff/reception/walk-ins.html")

#Routes for doctors
@app.route("/doctor")
def doctor():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if 'roomid' in session:
        cursor.execute("select appointments.appointmentId, patients.patientId, patients.fullname, patients.number "
                       "from appointments inner join patients on appointments.patientId = patients.patientId "
                       "where appointments.roomNo = %s", session['roomid'])
        if cursor.rowcount == 0:
            flash("There are no appointments assigned to this room", "info")
            return render_template("staff/doctors/doctorsportal.html")
        else:
            rows = cursor.fetchall()
            return render_template("staff/doctors/doctorsportal.html", rows=rows)
    else:
        return render_template("staff/doctors/doctorsportal.html")


@app.route("/room", methods=['POST', 'GET'])
def room():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        room = request.form['room']

        cursor.execute("select * from rooms where roomid = %s", room)
        if cursor.rowcount == 0:
            flash("The room number you entered does not exist, Try again", "info")
            return redirect("/doctor")
        elif cursor.rowcount == 1:
            session['roomid'] = room
            return redirect("/doctor")
        else:
            flash("Error occurred, try again", "danger")
            return redirect("/doctor")


@app.route("/treat/<id>", methods=['POST', 'GET'])
def treat(id):
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        # read the treatment id
        with open("myapp/db_ids/treatment_id", "r") as file:
            old_id = int(file.read())
            treatment_id = "T" + str(old_id)
        appointment_id = request.form['appointment_id']
        patient_id = request.form['patient_id']
        symptoms = request.form['symptoms']
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']

        cursor.execute("insert into treatment(treatmentid, patientid, appointmentid, symptoms, roomno, "
                       "diagnosis, Prescription, doctorid) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (treatment_id, patient_id, appointment_id, symptoms, session['roomid'], diagnosis, prescription,
                        session['staffId']))
        conn.commit()
        old_id += 1
        # Save the new treatment id to file
        with open("myapp/db_ids/treatment_id", "w") as file:
            file.write(str(old_id))
        flash("Record added successfully", "success")
        flash("Direct patient to phamarcist for medication", "info")
        return redirect(f"/treat/{id}")
    else:
        cursor.execute("select appointments.appointmentId, patients.patientId, patients.fullname, patients.number "
                       "from appointments inner join patients on appointments.patientId = patients.patientId "
                       "where appointments.appointmentId = %s", id)
        if cursor.rowcount == 0:
            flash("The id given does not exist", "danger")
            return redirect("/doctor")
        elif cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("staff/doctors/treat.html", rows=rows)

@app.route("/treated_patients")
def treated_patients():

    return render_template("staff/doctors/treated.html")

# Route for the staff logout page
@app.route("/logout_staff")
def logout_staff():
    session.pop('staffId', None)
    session.pop('roomid', None)
    return redirect("/staff_login")
