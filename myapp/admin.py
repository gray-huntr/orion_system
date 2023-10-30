from myapp import myapp as app
from flask import render_template, request, flash, redirect, render_template
import pymysql
# connect to database
conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                       password=app.config["DB_PASSWORD"],
                       database=app.config["DB_NAME"])


# Route for the admin page
@app.route("/admin")
def admin():
    return render_template("admin/admin.html")


@app.route("/staff_management/<action>", methods=['POST','GET'])
def staff_management(action):
    if action == 'add':
        if request.method == 'POST':
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
                cursor.execute("insert into staff(fullName, email, number, password, category) values (%s,%s,%s,%s,%s)",
                               (name,email,number,password,category))
                conn.commit()
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