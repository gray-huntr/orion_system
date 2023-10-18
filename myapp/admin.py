from myapp import myapp

from flask import render_template
# Route for the admin page
@myapp.route("/admin")
def admin():
    return render_template("admin/admin.html")