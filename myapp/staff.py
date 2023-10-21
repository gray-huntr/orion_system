from myapp import myapp, server, patient
from flask import render_template, request, redirect
from datetime import datetime

cursor = server.connect()

# Route for the staff page
@myapp.route("/staff")
def staff():
    return render_template("staff/staff.html")

@myapp.route("/admit", methods=['POST', 'GET'])
def admit():
    if request.method == 'POST':
        fullname = request.form['fullname'] 
        email = request.form['email']
        password = request.form['password']
        repeatPassword = request.form['repeatPassword']
        phoneNumber = request.form['phoneNumber']
        homeAddress = request.form['homeAddress']
        age = request.form['age']
        sex = request.form['sex']
        idNumber = request.form['idNumber']
        kinFullname = request.form['kinFullname']
        kinPhoneNumber = request.form['kinPhoneNumber']
        kinHomeAddress = request.form['kinHomeAddress']
        kinAge = request.form['kinAge']
        kinSex = request.form['kinSex']
        roomNo = request.form['roomNo']
        Diagnosis = request.form['Diagnosis']
        dateAdmitted = request.form['dateAdmitted']
        patient_data = patient.Patient(fullname, email, password, phoneNumber,"", homeAddress,age,sex,idNumber,kinFullname,kinPhoneNumber,kinHomeAddress,kinAge,kinSex,roomNo,Diagnosis,dateAdmitted, isDischarged=0, isTreated=0, isAdmitted=1, dischargedDate=datetime.utcnow(), prescription="")
        if server.admit_patient(cursor, patient_data):
            return "Success"
        else:
            return "Failure"
