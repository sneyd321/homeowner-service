import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    def __init__(self, app):
        self.app = app


    def productionConfig(self):    
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@homeowner-db.default.svc.cluster.local:3306/roomr"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["SECRET_KEY"] = "SECCCCCCCCCCCCCCCCCCCCCCCCRET"
        return self.app

    def developmentConfig(self):    
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:admin@homeowner-db:3306/roomr"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["SECRET_KEY"] = "SECCCCCCCCCCCCCCCCCCCCCCCCRET"
        return self.app

    def testConfig(self):
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'test.db')
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["SECRET_KEY"] = "SECCCCCCCCCCCCCCCCCCCCCCCCRET"
        return self.app