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
    phoneNumber = db.Column(db.String(15))
    isComplete = db.Column(db.Boolean())
    
    def __init__(self, **kwargs):
        """**kwargs firstName, lastName, email, password, phoneNumber"""
        self.firstName = kwargs.get("firstName", "")
        self.lastName = kwargs.get("lastName", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.imageURL = None
        self.phoneNumber = kwargs.get("phoneNumber", "")
        self.isComplete = False
        

    def generatePasswordHash(self, password):
        self.password = generate_password_hash(password)
    
    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            db.session.close()
            return False

    def close_session(self):
        db.session.close()

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
            Homeowner.phoneNumber: self.phoneNumber
        }

    def toJson(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
            "imageURL": self.imageURL,
            "homeownerLocation": HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.id).first().toJson() if HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.id).first() else None
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



class HomeownerLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100), )
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitNumber = db.Column(db.String(10))
    poBox = db.Column(db.String(10))
    homeownerId = db.Column(db.Integer(), nullable=False)

    def __init__(self, **homeownerLocationData):
        self.streetNumber = homeownerLocationData.get("streetNumber", "")
        self.streetName = homeownerLocationData.get("streetName", "")
        self.city = homeownerLocationData.get("city", "")
        self.province = homeownerLocationData.get("province", "")
        self.postalCode = homeownerLocationData.get("postalCode", "")
        self.unitNumber = homeownerLocationData.get("unitNumber", "")
        self.poBox = homeownerLocationData.get("poBox", "")
        self.homeownerId = homeownerLocationData.get("homeownerId", "")

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return False

    def update(self):
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).update(self.toDict(), synchronize_session=False)
        db.session.commit()

    def delete(self):
        HomeownerLocation.query.filter(HomeownerLocation.homeownerId == self.homeownerId).delete()
        db.session.commit()

    def toDict(self):
        return {
            HomeownerLocation.streetNumber: self.streetNumber,
            HomeownerLocation.streetName: self.streetName,
            HomeownerLocation.city: self.city,
            HomeownerLocation.province: self.province,
            HomeownerLocation.postalCode: self.postalCode,
            HomeownerLocation.unitNumber: self.unitNumber,
            HomeownerLocation.poBox: self.poBox
        }

    def toJson(self):
        return {
            "streetNumber": self.streetNumber,
            "streetName": self.streetName,
            "city": self.city,
            "province": self.province,
            "postalCode": self.postalCode,
            "unitNumber": self.unitNumber,
            "poBox": self.poBox
        }

    def __repr__(self):
        return "< Homeowner Location: " + str(self.streetNumber) + " " + self.streetName + " >"