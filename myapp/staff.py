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
                        return render_template("staff/doctor/doctorsPortal.html")
                    elif category == "Receptionist":
                        return render_template("staff/reception/receptionist.html")
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
                    cursor.execute("update patients set firstLogin = '0', password = %s where patientId = %s", (new_password,session['patientId']))
                    conn.commit()
                    flash("Password changed successfully", "success")
                    return redirect("/")
                else:
                    flash("New passwords do not match", "danger")
                    return redirect("/password_change")
    else:
        return render_template("password_change.html ")

# Route for the staff page
# @app.route("/staff")
# def staff():
#     return render_template("staff/staff_login.html")
