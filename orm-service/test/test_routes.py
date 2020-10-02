import unittest
from server import create_app, db
from server.api.Models import *
import json, time

class FlaskClientTestCase(unittest.TestCase):    
    def setUp(self):        
        self.app = create_app("test")    
        self.app_context = self.app.app_context()        
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)  
        
    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        
    #********************************TEST CREATE HOMEOWNER*******************************************************
    def test_insert_homeowner(self):
        payload = self.create_homeowner_account_request()
        headers = { "Content-Type": "application/json" }
        response = self.client.post('/api/v1/Homeowner', data=json.dumps(payload), headers=headers)        
        self.assertEqual(response.status_code, 200, "Error inserting check save() method in homeowner")  
    

    def test_insert_duplicate_homeowner(self):
        payload = self.create_homeowner_account_request()
        headers = { "Content-Type": "application/json" }
        self.client.post('/api/v1/Homeowner', data=json.dumps(payload), headers=headers)  
        response = self.client.post('/api/v1/Homeowner', data=json.dumps(payload), headers=headers)   
        self.assertEqual(response.status_code, 409, "Error on catching Integrity Error in save() method in homeowner")  

    def test_insert_multiple_homeowners(self):
        payload1 = self.create_homeowner_account_request()
        headers = { "Content-Type": "application/json" }
        self.client.post('/api/v1/Homeowner', data=json.dumps(payload1), headers=headers)  
        payload2 = self.create_homeowner_account_request_2()
        response = self.client.post('/api/v1/Homeowner', data=json.dumps(payload2), headers=headers)   
        self.assertEqual(response.status_code, 200, "Error in save() method not adding two records")  

    #*********************************************************************************************************
    #***************************TEST GET HOMEOWNER***************************************************
    def test_get_homeowner(self):
        mockAccount = Homeowner(self.create_homeowner_account_request())
        mockAccount.save()
        response = self.client.get('/api/v1/Homeowner/rts1234567@hotmail.com')  
        self.assertEqual(response.status_code, 200)
 
 
    def test_get_homeowner_invalid_account(self):
        response = self.client.get('/api/v1/Homeowner/rts1234567@hotmail.com')  
        self.assertEqual(response.status_code, 401)





    def create_homeowner_account_request(self):
        return {
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": "rts1234567@hotmail.com",
            "password": "aaaaaa",
            "phoneNumber": "123 456 7890",
            "homeownerLocation": {
                    "streetNumber": 123,
                    "streetName": "Example St.",
                    "city": "Oakville",
                    "province": "Ontario",
                    "postalCode": "L6L 0E1",
                    "unitNumber": "207",
                    "poBox": "207" 
                }
        }    

    def create_homeowner_account_request_2(self):
        return {
            "firstName": "Ryan",
            "lastName": "Sneyd",
            "email": "new@email.com",
            "password": "aaaaaa",
            "phoneNumber": "123 456 7890",
            "homeownerLocation": {
                    "streetNumber": 123,
                    "streetName": "Example St.",
                    "city": "Oakville",
                    "province": "Ontario",
                    "postalCode": "L6L 0E1",
                    "unitNumber": "207",
                    "poBox": "207" 
                }
        }    


 

            

                   


   