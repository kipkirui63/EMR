
from api import jsonify, request, url_for,  Resource, User, make_response, send_from_directory,   db,   \
   Namespace,  uuid
from api import app, api
from .api_models import *
from .models import *
import os
from functools import wraps  
from flask_uploads import UploadSet, configure_uploads, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required, current_user
from flask import url_for
from datetime import  timedelta,datetime


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
jwt = JWTManager(app)
jwt.init_app(app)


authorizations = {
    "jwToken":{
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(__jwt__header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()



ns_auth = Namespace('authorization', description='related operations', authorizations=authorizations)
ns_payment = Namespace('payments', description='related operations',authorizations=authorizations)
ns_patient = Namespace('patient', description=' related operations',authorizations=authorizations)
ns_user = Namespace('users', description='User & Payment related operations',authorizations=authorizations)
ns_receptionist = Namespace('receptionist', description='Category related operations',authorizations=authorizations)
ns_doctor = Namespace('doctor', description=' related operations',authorizations=authorizations)
ns_nurse = Namespace('nurse', description='related operations',authorizations=authorizations)
ns_laboratorytechnician = Namespace('labtechnician', description=' related operations',authorizations=authorizations)
ns_manager = Namespace('manager', description=' operations', authorizations=authorizations)



api.add_namespace(ns_auth)
api.add_namespace(ns_payment)
api.add_namespace(ns_patient)
api.add_namespace(ns_receptionist)
api.add_namespace(ns_doctor)
api.add_namespace(ns_nurse)
api.add_namespace(ns_laboratorytechnician)
api.add_namespace(ns_user)
api.add_namespace(ns_manager)




# ----------------------------------------------------- G L O B A L  V A R I A B L E S -----------------------------------------------


paymentConfirmationDetails = []
print(paymentConfirmationDetails)


@ns_auth.route('/signup')
class Signup(Resource):
    @ns.expect(signup_input_schema)
    # @ns.marshal_with(users_schema)
    def post(self):
        data = request.get_json()
        print("signup",data)
        if not data:
            return {"message":"Data not found!"},404
        
        required_fields = ['username', 'email', 'password', 'repeatpassword', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or data[field]=='':
                return {'message': f'Missing required field: {field}'}, 400
            
        if data['password'] != data['repeatpassword']:
            return {'message': "Passwords Do No Match"}, 404
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            public_id=str(uuid.uuid4()),
            first_name = data['first_name'],
            last_name = data['last_name'],
        )      
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        print("new added user",new_user)

        user_dict = {
            key: getattr(new_user,key)
            for key in ["id","username", "email", "public_id", "first_name", "last_name"]
        }



@ns_auth.route('/login')
class Login(Resource):
    @ns.expect(user_login_schema)
    def post(self):
        data = request.get_json()

        if not data or not data['username'] or not data['password']:
            return {'message': 'Unable to verify user'}, 401

        user = User.query.filter_by(email=data['username']).first()

        if not user:
            return {'message': 'Authentication failed. Invalid username or password'}, 401
        




# ----------------------------------------------  P A Y M E N T   R O U T E S -----------------------------------------------

 
@ns_payment.route('/payment')
class MakePayment(Resource):
    @ns.marshal_with(payments_schema)
    def post(self):
        # TO RUN NGROK SERVER TO POPULATE PAYMENT TABLE: `ngrok http 5555 --domain redfish-prime-pigeon.ngrok-free.app`
        # CHANGE WEBHOOK IN TINYPESA IF DOMAIN CHANGES CURRENT DOMAIN: `redfish-prime-pigeon.ngrok-free.app`
        data = request.get_json()
        if 'Body' in data and 'stkCallback' in data['Body']:
            payment_details = data['Body']['stkCallback']
            if payment_details:
                keys_to_extract = ["ResultCode", "ResultDesc", "CallbackMetadata", "ExternalReference", "Amount", "Msisdn"]
                transaction_data = {
                    key: payment_details.get(key)
                    for key in keys_to_extract
                }
                print("!!!!!!Webhook received and processed successfully!!!!!!!")
                print(f"---------->Data:{transaction_data}")


            #  create payment record
            callback_metadata= transaction_data['CallbackMetadata']['Item']
            for item in callback_metadata:
                if item['Name'] == "Amount":
                    amount = item.get('Value')
                elif item['Name'] == "MpesaReceiptNumber":
                    mpesa_receipt_number = item.get('Value')
                elif item['Name'] == "TransactionDate":
                    transaction_date = item.get('Value')
                elif item['Name'] == "PhoneNumber":
                    phone_number = item.get('Value')

            new_payment = Payment(
                mpesa_receipt_code=mpesa_receipt_number,
                payment_date=transaction_date,
                paid_by_number=phone_number,
                amount_paid=amount,
                payment_uid=transaction_data['ExternalReference']
            )
            db.session.add(new_payment)
            db.session.commit() 

            
                

            return new_payment, 201
        else:
            return {'message': 'Invalid request data'}, 400


@ns_payment.route('/get_payment_confirmation_details')
class GetPaymentConfirmation(Resource):
    @ns.marshal_with(payments_schema)
    def get(self):
        payments = Payment.query.all()
        if payments:
            # print(f'-----------------> {payments}')
            return payments, 200
        else:
            return {'message': 'No payment confirmation data available'}, 404 
        

@ns_payment.route('/payments')
class Payments(Resource):
    def post(self):
        data = request.get_json()
        callback_metadata= data['CallbackMetadata']['Item']
        for item in callback_metadata:
            if item['Name'] == "Amount":
                amount = item.get('Value')
            elif item['Name'] == "MpesaReceiptNumber":
                mpesa_receipt_number = item.get('Value')
            elif item['Name'] == "TransactionDate":
                transaction_date = item.get('Value')
            elif item['Name'] == "PhoneNumber":
                phone_number = item.get('Value')

        new_payment = Payment(
            mpesa_receipt_code=mpesa_receipt_number,
            payment_date=transaction_date,
            paid_by_number=phone_number,
            amount_paid=amount,
            payment_uid=data.get('ExternalReference')  
        )
        db.session.add(new_payment)
        db.session.commit()     





# CRUD routes for Patient
@ns_patient.route('/patients')
class Patients(Resource):
    @ns_patient.marshal_with(patient_schema)
    def get(self):
        patients = Patient.query.all()
        return patients

    @ns_patient.expect(patient_schema)
    @ns_patient.marshal_with(patient_schema)
    def post(self):
        data = request.get_json()
        new_patient = Patient(**data)
        db.session.add(new_patient)
        db.session.commit()
        return new_patient, 201

@ns_patient.route('/patients/<int:id>')
class PatientDetail(Resource):
    @ns_patient.marshal_with(patient_schema)
    def get(self, id):
        patient = Patient.query.get(id)
        if not patient:
            api.abort(404, "Patient not found")
        return patient

    @ns_patient.expect(patient_schema)
    @ns_patient.marshal_with(patient_schema)
    def put(self, id):
        patient = Patient.query.get(id)
        if not patient:
            api.abort(404, "Patient not found")
        data = request.get_json()
        for key, value in data.items():
            setattr(patient, key, value)
        db.session.commit()
        return patient

    def delete(self, id):
        patient = Patient.query.get(id)
        if not patient:
            api.abort(404, "Patient not found")
        db.session.delete(patient)
        db.session.commit()
        return '', 204


# CRUD routes for Doctor
@ns_doctor.route('/doctors')
class Doctors(Resource):
    @ns_doctor.marshal_with(doctor_schema)
    def get(self):
        doctors = Doctor.query.all()
        return doctors

    @ns_doctor.expect(doctor_schema)
    @ns_doctor.marshal_with(doctor_schema)
    def post(self):
        data = request.get_json()
        new_doctor = Doctor(**data)
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor, 201

@ns_doctor.route('/doctors/<int:id>')
class DoctorDetail(Resource):
    @ns_doctor.marshal_with(doctor_schema)
    def get(self, id):
        doctor = Doctor.query.get(id)
        if not doctor:
            api.abort(404, "Doctor not found")
        return doctor

    @ns_doctor.expect(doctor_schema)
    @ns_doctor.marshal_with(doctor_schema)
    def put(self, id):
        doctor = Doctor.query.get(id)
        if not doctor:
            api.abort(404, "Doctor not found")
        data = request.get_json()
        for key, value in data.items():
            setattr(doctor, key, value)
        db.session.commit()
        return doctor

    def delete(self, id):
        doctor = Doctor.query.get(id)
        if not doctor:
            api.abort(404, "Doctor not found")
        db.session.delete(doctor)
        db.session.commit()
        return '', 204



# CRUD routes for Receptionist
@ns_receptionist.route('/receptionists')
class Receptionists(Resource):
    @ns_receptionist.marshal_with(receptionist_schema)
    def get(self):
        receptionists = Receptionist.query.all()
        return receptionists

    @ns_receptionist.expect(receptionist_schema)
    @ns_receptionist.marshal_with(receptionist_schema)
    def post(self):
        data = request.get_json()
        new_receptionist = Receptionist(**data)
        db.session.add(new_receptionist)
        db.session.commit()
        return new_receptionist, 201

@ns_receptionist.route('/receptionists/<int:id>')
class ReceptionistDetail(Resource):
    @ns_receptionist.marshal_with(receptionist_schema)
    def get(self, id):
        receptionist = Receptionist.query.get(id)
        if not receptionist:
            api.abort(404, "Receptionist not found")
        return receptionist

    @ns_receptionist.expect(receptionist_schema)
    @ns_receptionist.marshal_with(receptionist_schema)
    def put(self, id):
        receptionist = Receptionist.query.get(id)
        if not receptionist:
            api.abort(404, "Receptionist not found")
        data = request.get_json()
        for key, value in data.items():
            setattr(receptionist, key, value)
        db.session.commit()
        return receptionist

    def delete(self, id):
        receptionist = Receptionist.query.get(id)
        if not receptionist:
            api.abort(404, "Receptionist not found")
        db.session.delete(receptionist)
        db.session.commit()
        return '', 204


# Payment routes
@ns_payment.route('/payments')
class Payments(Resource):
    @ns_payment.marshal_with(payments_schema)
    def get(self):
        payments = Payment.query.all()
        return payments

    @ns_payment.expect(payment_schema)
    @ns_payment.marshal_with(payment_schema)
    def post(self):
        data = request.get_json()
        new_payment = Payment(**data)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment, 201

@ns_payment.route('/payments/<int:id>')
class PaymentDetail(Resource):
    @ns_payment.marshal_with(payment_schema)
    def get(self, id):
        payment = Payment.query.get(id)
        if not payment:
            api.abort(404, "Payment not found")
        return payment

    @ns_payment.expect(payment_schema)
    @ns_payment.marshal_with(payment_schema)
    def put(self, id):
        payment = Payment.query.get(id)
        if not payment:
            api.abort(404, "Payment not found")
        data = request.get_json()
        for key, value in data.items():
            setattr(payment, key, value)
        db.session.commit()
        return payment

    def delete(self, id):
        payment = Payment.query.get(id)
        if not payment:
            api.abort(404, "Payment not found")
        db.session.delete(payment)
        db.session.commit()
        return '', 204
