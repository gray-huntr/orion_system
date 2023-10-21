from myapp import myapp as app
import pymysql


def connect():
    conn = pymysql.connect(host=app.config["DB_HOST"], user=app.config["DB_USERNAME"],
                           password=app.config["DB_PASSWORD"], database=app.config["DB_NAME"])
    return conn.cursor()


def authenticate(cursor, email, password):
    cursor.execute(f"select * from credentials where email = %s and password = %s", (email, password))
    user = cursor.fetchone()
    if user:
        user_info = {
            "id" : user[0],
            "isAdmin" : user[4],
            "isStaff" : user[5],
            "isPatient" : user[6]
        }
        return user_info
    return None


def signup(cursor, fullname, email, password):
    try:
        cursor.execute("insert into credentials (fullname, email, password) values (%s , %s, %s)",
                       (fullname, email, password))
        cursor.connection.commit()
        return True
    except pymysql.IntegrityError:
        return False
    
def search_for_patient(cursor, id):
    patient = cursor.execute("select * from patients where id = %s", (id))
    patient = cursor.fetchone()
    if patient:
        patient_dict = {
            "fullname": patient[1],
            "roomNo": patient[2],
            "diagnosis": patient[3],
            "email": patient[4],
        }
        print(patient_dict)
        return patient_dict
    return None

def admit_patient(cursor, patient):
    try:
        query = """
            INSERT INTO patients (fullname, email, telephoneNo, homeAddress, age, sex, nationalId, relativefullname,
                                  relativephoneno, relativeAddress, relativeAge, relativeSex, room_no, diagnosis, dateAdmitted,
                                  isAdmitted, isDischarged, isTreated, dischargedDate, prescription)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            patient.fullname, patient.email, patient.phoneNumber, patient.homeAddress, patient.age, patient.sex,
            patient.idNumber, patient.kinFullname, patient.kinPhoneNumber, patient.kinHomeAddress, patient.kinAge,
            patient.kinSex, patient.roomNo, patient.Diagnosis, patient.dateAdmitted, patient.isAdmitted, patient.isDischarged, 
            patient.isTreated, patient.dischargedDate, patient.prescription
        )

        cursor.execute(query, values)
        cursor.connection.commit()
        return True
    except pymysql.IntegrityError:
        return False

