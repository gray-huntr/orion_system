from myapp import myapp as app
from flask import render_template, request, flash, redirect
import pymysql

# connect to database
conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                       password=app.config["DB_PASSWORD"],
                       database=app.config["DB_NAME"])

@app.route("/staff_login", methods=['POST', 'GET'])
def staff_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor()
        cursor.execute("select * from staff where email = %s and password = %s",(email,password))
        if cursor.rowcount == 0:
            flash("Incorrect username or password, try again", "warning")
            return redirect("/staff_login")
        elif cursor.rowcount == 1:
            return redirect("/")
        else:
            flash("Error occurred", "danger")
            return redirect("/staff_login")
    else:
        return render_template("staff/staff_login.html")
# Route for the staff page
# @app.route("/staff")
# def staff():
#     return render_template("staff/staff_login.html")
