from myapp import myapp

from flask import render_template


# Route for the staff page
@myapp.route("/staff")
def staff():
    return render_template("staff/staff.html")
