from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, UniqueConstraint, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import bcrypt
#from api import generate_password_hash

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    profile_pic = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

 


    __table_args__ = (
    UniqueConstraint('username', name='user_unique_constraint'),
    UniqueConstraint('email', name='email_unique_constraint')
    )


    def __repr__(self):
        return f'(id={self.id}, name={self.username} email={self.email} profile_pic={self.profile_pic})'

   
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))



class Patient(db.Model):
    PatientID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    DateOfBirth = db.Column(db.Date)
    Gender = db.Column(db.String(10))
    ContactNumber = db.Column(db.String(15))
    Address = db.Column(db.String(255))

class Receptionist(db.Model):
    ReceptionistID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class Doctor(db.Model):
    DoctorID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Specialization = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class Nurse(db.Model):
    NurseID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Specialization = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class LaboratoryTechnician(db.Model):
    LabTechID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Specialization = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class Pharmacist(db.Model):
    PharmacistID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    DoctorID = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'))

class Manager(db.Model):
    ManagerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    ReceptionistID = db.Column(db.Integer, db.ForeignKey('receptionist.ReceptionistID'))
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'))
    AppointmentDate = db.Column(db.DateTime)
    Status = db.Column(db.String(20))

class Consultation(db.Model):
    ConsultationID = db.Column(db.Integer, primary_key=True)
    NurseID = db.Column(db.Integer, db.ForeignKey('nurse.NurseID'))
    DoctorID = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'))
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'))
    ConsultationDate = db.Column(db.DateTime)

class LabTest(db.Model):
    TestID = db.Column(db.Integer, primary_key=True)
    LabTechID = db.Column(db.Integer, db.ForeignKey('laboratory_technician.LabTechID'))
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'))
    DoctorID = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'))
    TestName = db.Column(db.String(100))
    TestDate = db.Column(db.DateTime)
    Results = db.Column(db.String(255))

class Medication(db.Model):
    MedicationID = db.Column(db.Integer, primary_key=True)
    PharmacistID = db.Column(db.Integer, db.ForeignKey('pharmacist.PharmacistID'))
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'))
    DoctorID = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'))
    MedicationName = db.Column(db.String(100))
    DispenseDate = db.Column(db.DateTime)

class Payment(db.Model):
    PaymentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'))
    Amount = db.Column(db.Float)
    Date = db.Column(db.DateTime)
    PaymentStatus = db.Column(db.String(20))


