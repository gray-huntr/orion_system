class Patient:
    def __init__(self, fullname, email, password, repeatPassword, phoneNumber, homeAddress, age, sex, idNumber,
                 kinFullname, kinPhoneNumber, kinHomeAddress, kinAge, kinSex, roomNo, Diagnosis, dateAdmitted, 
                 isAdmitted, isTreated, isDischarged, dischargedDate, prescription):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.repeatPassword = repeatPassword
        self.phoneNumber = phoneNumber
        self.homeAddress = homeAddress
        self.age = age
        self.sex = sex
        self.idNumber = idNumber
        self.kinFullname = kinFullname
        self.kinPhoneNumber = kinPhoneNumber
        self.kinHomeAddress = kinHomeAddress
        self.kinAge = kinAge
        self.kinSex = kinSex
        self.roomNo = roomNo
        self.Diagnosis = Diagnosis
        self.dateAdmitted = dateAdmitted
        self.isAdmitted = isAdmitted
        self.isTreated = isTreated
        self.isDischarged = isDischarged
        self.dischargedDate = dischargedDate
        self.prescription = prescription
