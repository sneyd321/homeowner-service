from werkzeug.security import generate_password_hash, check_password_hash
from server import db, app
from sqlalchemy.exc import IntegrityError, OperationalError
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Homeowner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(100))
    imageURL = db.Column(db.String(250), nullable=True)
    taskId = db.Column(db.String(40), nullable=True)
    phoneNumber = db.Column(db.String(15))
    
    def __init__(self, **kwargs):
        """**kwargs firstName, lastName, email, password, phoneNumber"""
        self.firstName = kwargs.get("firstName", "")
        self.lastName = kwargs.get("lastName", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.imageURL = None
        self.taskId = None
        self.phoneNumber = kwargs.get("phoneNumber", "")
        

    def generatePasswordHash(self, password):
        self.password = generate_password_hash(password)
    
    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            db.session.close()
            return False

    def update(self):
        rows = Homeowner.query.filter(Homeowner.email == self.email).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                db.session.commit()
                db.session.close()
                return True
            except OperationalError:
                db.session.rollback()
                db.session.close()
                return False
        return False

    def delete(self):
        try:
            Homeowner.query.filter(Homeowner.email == self.email).delete()
            db.session.commit()
            db.session.close()
            return True
        except IntegrityError:
            print("Error")
            db.session.rollback()
            db.session.close()
            return False

        

    def toDict(self):
        return {
            Homeowner.firstName: self.firstName,
            Homeowner.lastName: self.lastName,
            Homeowner.email: self.email,
            Homeowner.password: self.password,
            Homeowner.imageURL: self.imageURL,
            Homeowner.taskId: self.taskId,
            Homeowner.phoneNumber: self.phoneNumber
        }

    def toJson(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "imageURL": self.imageURL,
            "taskId": self.taskId
        }

    def getAuthToken(self):
         return {
            "authToken": self.generate_auth_token().decode("utf-8")
        }

    def getId(self):
        return {
            "homeownerId": self.id
        }

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            return Homeowner.query.get(data['id'])
        except SignatureExpired:
            return None 
        except BadSignature:
            return None # invalid token
        
        

    def __repr__(self):
        return "< Homeowner: " + self.firstName + " " + self.lastName + " >"


