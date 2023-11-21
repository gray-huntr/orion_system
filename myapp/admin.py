from myapp import myapp as app
from flask import render_template, request, flash, redirect, render_template, make_response
import pymysql
from fpdf import FPDF


# Route for the admin page
@app.route("/client_management")
def admin():
    return render_template("admin/client_management.html")


@app.route("/reports")
def reports():
    return render_template("admin/reports.html")



@app.route("/staff_management/<action>", methods=['POST', 'GET'])
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
                               (staff_id, name, email, number, password, category))
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


@app.route("/client_management", methods=['POST', 'GET'])
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
    cursor.execute(
        "select billing.billingid, patients.fullname, billing.appointmentid, billing.test_cost, billing.total,"
        "staff.fullname, billing.date from billing inner join patients on billing.patientId = patients.patientId inner join staff "
        "on billing.cashier_id = staff.staffId")
    rows = cursor.fetchall()
    return render_template("admin/billings.html", rows=rows)


@app.route("/search/<category>", methods=['POST', 'GET'])
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
    elif category == 'billing':
        cursor.execute(
            "select billing.billingid, patients.fullname, billing.appointmentid, billing.test_cost, billing.total,"
            "staff.fullname, billing.date from billing inner join patients on billing.patientId = patients.patientId inner join staff "
            "on billing.cashier_id = staff.staffId where billing.billingid = %s or patients.fullname like %s or staff.fullname like %s",
            (search_term, '%' + search_term + '%', '%' + search_term + '%'))
        if cursor.rowcount > 0:
            rows = cursor.fetchall()
            return render_template("admin/billings.html", rows=rows)
        elif cursor.rowcount == 0:
            flash("There is no record with the specified search term, try again", "info")
            return redirect("/billing")


@app.route("/report/<category>")
def report(category):
    # connect to database
    global output
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"],
                           database=app.config["DB_NAME"])
    cursor = conn.cursor()

    if category == 'clients':
        cursor.execute("select * from patients")
        rows = cursor.fetchall()

        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.set_font("Times", size=12)

        # Table headers
        headers = ["Patient ID", "Patient name", "Email", "Number", "Gender", "DOB", "Blood group"]
        pdf.set_fill_color(200, 220, 255)
        # Set the column widths
        col_widths = [40, 40, 60, 40, 30, 30, 30]

        for header, width in zip(headers, col_widths):
            pdf.cell(width, 10, header, 1)
        pdf.ln()

        # Table data
        for row in rows:
            data_row = [row[0], row[1], row[2], row[3], row[6], str(row[7]), row[8]]

            # Convert None values to empty strings
            data_row = ["" if val is None else val for val in data_row]

            # Add data to the table
            for datum, width in zip(data_row, col_widths):
                pdf.cell(width, 10, datum, 1)
            pdf.ln()

        # Save the PDF
        # pdf.output(f"{category}.pdf")
        output = bytes(pdf.output(dest='S'))
    elif category == 'staff':
        cursor.execute("select * from staff")
        rows = cursor.fetchall()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=12)
        # Table headers
        headers = ["Staff ID", "name", "Email", "Number"]
        pdf.set_fill_color(200, 220, 255)

        # Set the column widths
        col_widths = [40, 40, 60, 40]

        for header, width in zip(headers, col_widths):
            pdf.cell(width, 10, header, 1)
        pdf.ln()

        # Table data
        for row in rows:
            data_row = [row[0], row[1], row[2], row[3]]

            # Convert None values to empty strings
            data_row = ["" if val is None else val for val in data_row]

            # Add data to the table
            for datum, width in zip(data_row, col_widths):
                pdf.cell(width, 10, datum, 1)
            pdf.ln()

        # Save the PDF
        # pdf.output(f"{category}.pdf")
        output = bytes(pdf.output(dest='S'))
    elif category == 'appointments':
        cursor.execute(
            "select appointments.appointmentId, appointments.patientId, appointments.roomno, appointments.time, "
            "appointments.status, patients.fullname from appointments inner join patients on "
            "appointments.patientId = patients.patientId")
        rows = cursor.fetchall()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=12)
        # Table headers
        headers = ["Appointment ID", "Patient ID", "Patient Name", "Room number", "Date/time", "status"]
        pdf.set_fill_color(200, 220, 255)

        # Set the column widths
        col_widths = [30, 30, 30, 30, 40, 30]

        for header, width in zip(headers, col_widths):
            pdf.cell(width, 10, header, 1)
        pdf.ln()

        # Table data
        for row in rows:
            data_row = [row[0], row[1], row[5], row[2], str(row[3]), row[4]]

            # Convert None values to empty strings
            data_row = ["" if val is None else val for val in data_row]

            # Add data to the table
            for datum, width in zip(data_row, col_widths):
                pdf.cell(width, 10, datum, 1)
            pdf.ln()

        # Save the PDF
        # pdf.output(f"{category}.pdf")
        output = bytes(pdf.output(dest='S'))
    response = make_response(output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={category}.pdf'
    return response


# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
