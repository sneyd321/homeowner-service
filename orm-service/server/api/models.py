from werkzeug.security import generate_password_hash, check_password_hash
from server import db
from sqlalchemy.exc import IntegrityError, OperationalError

class Homeowner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(15))
    token = db.Column(db.String(38))
    homeownerLocation = db.relationship('HomeownerLocation', backref='homeowner', lazy=True, uselist=False)
    
    def __init__(self, homeownerData):
        self.firstName = homeownerData["firstName"]
        self.lastName = homeownerData["lastName"]
        self.email = homeownerData["email"]
        self.password = homeownerData["password"]
        self.phoneNumber = homeownerData["phoneNumber"]
        self.token = homeownerData["token"]
        self.homeownerLocation = HomeownerLocation(homeownerData["homeownerLocation"])


    def generatePasswordHash(self, password):
        self.password = generate_password_hash(password)
    
    def verifyPassword(self, password):
        return check_password_hash(self.password, password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    def update(self):
        rows = Homeowner.query.filter(Homeowner.email == self.email).update(self.toDict(), synchronize_session=False)
        if rows == 1:
            try:
                self.homeownerLocation.update()
                db.session.commit()
                return True
            except OperationalError:
                db.session.rollback()
                return False
        return False
        

    def toDict(self):
        return {
            Homeowner.firstName: self.firstName,
            Homeowner.lastName: self.lastName,
            Homeowner.email: self.email,
            Homeowner.password: self.password,
            Homeowner.phoneNumber: self.phoneNumber,
            Homeowner.token: self.token
        }

    def toJson(self):
        return {
            "homeownerId": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "homeownerLocation": self.homeownerLocation.toJson()
        }


    def __repr__(self):
        return "< Homeowner: " + self.firstName + " " + self.lastName + " >"

class HomeownerLocation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    streetNumber = db.Column(db.Integer())
    streetName = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    postalCode = db.Column(db.String(10))
    unitNumber = db.Column(db.String(10))
    poBox = db.Column(db.String(10))
    homeownerId = db.Column(db.Integer(), db.ForeignKey('homeowner.id'), nullable=False)

    def __init__(self, homeownerLocationData):
        self.streetNumber = homeownerLocationData["streetNumber"]
        self.streetName = homeownerLocationData["streetName"]
        self.city = homeownerLocationData["city"]
        self.province = homeownerLocationData["province"]
        self.postalCode = homeownerLocationData["postalCode"]
        self.unitNumber = homeownerLocationData["unitNumber"]
        self.poBox = homeownerLocationData["poBox"]

    
    def update(self):
        HomeownerLocation.query.update(self.toDict(), synchronize_session=False)
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