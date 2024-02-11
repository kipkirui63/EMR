from api import fields, api, ma
from marshmallow import Schema, fields
from flask_restx import Api,Resource,Namespace,fields

ns = Namespace('EMR')
api.add_namespace(ns)

# ------------------------- A P I _ M O D E L S ------------------------

users_summary_schema = api.model('users',{
    "public_id": fields.String,
    "username": fields.String,
    "email": fields.String,
    "profile_pic": fields.String
    
})

users_schema = api.model('users',{
    "public_id": fields.String,
    "username": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "address": fields.String,
    "phone_number": fields.String,
    
})




user_input_schema = api.model('user_input',{
    "username": fields.String,
    "password": fields.String,
    "repeatpassword": fields.String,
    "email": fields.String,
    "profile_pic": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "address": fields.String,
    "phone_number": fields.String,
})

signup_input_schema = api.model('signup_input',{
    "username": fields.String,
    "password": fields.String,
    "repeatpassword": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    
})

user_login_schema = api.model('user_login',{
    "username": fields.String,
    "password": fields.String,

})

category_input_schema = api.model('category_input',{
    "name": fields.String,
    'image': fields.String
})




patient_schema = api.model('Patient', {
    'PatientID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'DateOfBirth': fields.Date,
    'Gender': fields.String,
    'ContactNumber': fields.String,
    'Address': fields.String
})

receptionist_schema = api.model('Receptionist', {
    'ReceptionistID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String
})

doctor_schema = api.model('Doctor', {
    'DoctorID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'Specialization': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String
})

nurse_schema = api.model('Nurse', {
    'NurseID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'Specialization': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String
})

lab_technician_schema = api.model('LaboratoryTechnician', {
    'LabTechID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'Specialization': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String
})

pharmacist_schema = api.model('Pharmacist', {
    'PharmacistID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String,
    'DoctorID': fields.Integer
})

manager_schema = api.model('Manager', {
    'ManagerID': fields.Integer,
    'FirstName': fields.String,
    'LastName': fields.String,
    'ContactNumber': fields.String,
    'Email': fields.String
})

appointment_schema = api.model('Appointment', {
    'AppointmentID': fields.Integer,
    'ReceptionistID': fields.Integer,
    'PatientID': fields.Integer,
    'AppointmentDate': fields.DateTime,
    'Status': fields.String
})

consultation_schema = api.model('Consultation', {
    'ConsultationID': fields.Integer,
    'NurseID': fields.Integer,
    'DoctorID': fields.Integer,
    'PatientID': fields.Integer,
    'ConsultationDate': fields.DateTime
})

lab_test_schema = api.model('LabTest', {
    'TestID': fields.Integer,
    'LabTechID': fields.Integer,
    'PatientID': fields.Integer,
    'DoctorID': fields.Integer,
    'TestName': fields.String,
    'TestDate': fields.DateTime,
    'Results': fields.String
})

medication_schema = api.model('Medication', {
    'MedicationID': fields.Integer,
    'PharmacistID': fields.Integer,
    'PatientID': fields.Integer,
    'DoctorID': fields.Integer,
    'MedicationName': fields.String,
    'DispenseDate': fields.DateTime
})

payment_schema = api.model('Payment', {
    'PaymentID': fields.Integer,
    'PatientID': fields.Integer,
    'Amount': fields.Float,
    'Date': fields.DateTime,
    'PaymentStatus': fields.String
})

payments_schema = api.model('Payment', {
    'PaymentID': fields.Integer,
    'PatientID': fields.Integer,
    'Amount': fields.Float,
    'Date': fields.DateTime,
    'PaymentStatus': fields.String
})





