from myapp import myapp as app
from flask import render_template, request, flash, redirect, render_template
import pymysql



# Route for the admin page
@app.route("/admin")
def admin():
    return render_template("admin/admin.html")


@app.route("/staff_management/<action>", methods=['POST','GET'])
def staff_management(action):
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    if action == 'add':
        if request.method == 'POST':
            with open("myapp/db_ids/staff_id", "r") as file:
                old_id = int(file.read())
                staff_id = "S" + str(old_id)
            name = request.form['name']
            email = request.form['email']
            number = request.form['number']
            password = "Orion@default"
            category = request.form['category']

            cursor = conn.cursor()
            cursor.execute("select email from staff where email = %s ", email)
            if cursor.rowcount > 0:
                flash("The email address already exists, use another one", "info")
                return redirect("/staff_management/add")
            elif cursor.rowcount == 0:
                cursor.execute("insert into staff(staffId, fullName, email, number, password, category) "
                               "values (%s,%s,%s,%s,%s,%s)",
                               (staff_id,name,email,number,password,category))
                conn.commit()
                old_id += 1
                # Save the new appointment id to file
                with open("myapp/db_ids/staff_id", "w") as file:
                    file.write(str(old_id))
                flash("Record added successfully", "success")
                return redirect("/staff_management/add")
        else:
            cursor = conn.cursor()
            cursor.execute("select * from staff")
            if cursor.rowcount == 0:
                flash("There are currently no records in the system", "info")
                return render_template("admin/staff_management.html")
            elif cursor.rowcount > 0:
                rows = cursor.fetchall()
                return render_template("admin/staff_management.html", rows=rows)
            else:
                flash("Error occurred try again", "danger")
                return render_template("admin/staff_management.html")
    elif action == 'update':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        category = request.form['category']

        cursor = conn.cursor()
        cursor.execute("update staff set fullName=%s, email = %s, number = %s, category = %s where staffId = %s",
                       (name, email, number, category, id))
        conn.commit()
        flash("Record updated successfully", "success")
        return redirect("/staff_management/add")


@app.route("/client_management", methods=['POST','GET'])
def client_management():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['id']
        status = request.form['status']

        cursor.execute("update patients set status = %s where patientId = %s", (status, id))
        conn.commit()
        flash("Patient status updated successfully", "info")
        return redirect("/client_management")
    else:
        cursor.execute("select * from patients")
        if cursor.rowcount == 0:
            flash("There are no patients in the database", "info")
            return render_template("admin/client_management.html")
        else:
            rows = cursor.fetchall()
            return render_template("admin/client_management.html", rows=rows)

@app.route("/appointment_management")
def appointment_management():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select appointments.appointmentId, appointments.patientId, appointments.roomno, appointments.time, "
                   "appointments.status, patients.fullname from appointments inner join patients on "
                   "appointments.patientId = patients.patientId")
    rows = cursor.fetchall()
    return render_template("admin/appointment_management.html", rows=rows)

@app.route("/treatment_records")
def treatment_records():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select treatment.treatmentid, patients.fullname, treatment.appointmentid, treatment.symptoms, "
                   "treatment.diagnosis, treatment.prescription, treatment.test_done, staff.fullname from treatment inner "
                   "join patients on treatment.patientId = patients.patientId inner join staff on staff.staffId = treatment.doctorid")
    rows = cursor.fetchall()
    return render_template("admin/treatment_records.html", rows=rows)


@app.route("/billing")
def billing():
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    cursor.execute("select billing.billingid, patients.fullname, billing.appointmentid, billing.test_cost, billing.total,"
                   "staff.fullname, billing.date from billing inner join patients on billing.patientId = patients.patientId inner join staff "
                   "on billing.cashier_id = staff.staffId")
    rows = cursor.fetchall()
    return render_template("admin/billings.html", rows=rows)


@app.route("/search/<category>", methods=['POST','GET'])
def search(category):
    # connect to database
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()
    search_term = request.form['search_term']
    if category == 'client':
        cursor.execute("select * from patients where patientId = %s or fullname like %s",
                       (search_term, '%' + search_term + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("admin/client_management.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("There is no record with the specified search term, try again", "info")
            return redirect("/client_management")
    elif category == 'staff':
        cursor.execute("select * from staff where staffId = %s or fullname like %s",
                       (search_term, '%' + search_term + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("admin/staff_management.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("There is no record with the specified search term, try again", "info")
            return redirect("/staff_management/add")
    elif category == 'appointment':
        cursor.execute(
            "select appointments.appointmentId, appointments.patientId, appointments.roomno, appointments.time, "
            "appointments.status, patients.fullname from appointments inner join patients on "
            "appointments.patientId = patients.patientId where appointments.appointmentId = %s or patients.patientId"
            " = %s or patients.fullname like %s", (search_term, search_term, '%' + search_term + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("admin/appointment_management.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("There is no record with the specified search term, try again", "info")
            return redirect("/appointment_management")
    elif category == 'treatment':
        cursor.execute("select treatment.treatmentid, patients.fullname, treatment.appointmentid, treatment.symptoms, "
                       "treatment.diagnosis, treatment.prescription, treatment.test_done, staff.fullname from treatment inner "
                       "join patients on treatment.patientId = patients.patientId inner join staff on staff.staffId = treatment.doctorid "
                       "where treatment.treatmentid = %s or patients.patientId = %s or patients.fullname like %s",
                       (search_term, search_term, '%' + search_term + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("admin/treatment_records.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("There is no record with the specified search term, try again", "info")
            return redirect("/treatment_records")



