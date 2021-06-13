import unittest
from server import create_app, SQLAlchemy
from server.api.models import *
import json, time

class FlaskClientTestCase(unittest.TestCase):    
    def setUp(self):        
        self.app = create_app("dev")    
        db = SQLAlchemy(self.app, {
            'expire_on_commit': False
        })
        db.create_all()
        self.app_context = self.app.app_context()        
        self.app_context.push()
        
        
        
    def tearDown(self):
        db.drop_all()
        
        self.app_context.pop()
        
    


 

            

                   


   