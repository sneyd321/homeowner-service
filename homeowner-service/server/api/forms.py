from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

  
class HomeownerForm(FlaskForm):
    firstName = StringField('First Name', 
    validators=[InputRequired("Please enter a first name"), Length(min=1, max=100, message="Please enter a name less that 100 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. John", "type": "text"})

    lastName = StringField('Last Name' , 
    validators=[InputRequired("Please enter a last name"), Length(min=1, max=100, message="Please enter a name less that 100 characters.")], 
    render_kw={"icon": "account_circle", "required": False, "helperText": "Ex. Smith", "type": "text"})

    email = StringField('Email', 
    validators=[InputRequired("Please enter an email"), Email("Please enter a valid email")],
    render_kw={"icon": "email", "required": False, "helperText": "Ex. name@example.com", "type": "email"})

    phoneNumber = StringField("Phone Number",
    validators=[InputRequired("Please enter a phone number")],
    render_kw={"icon": "smartphone", "required": False, "helperText": "Ex. 123-456-7890", "type": "tel"})


    password = PasswordField("Password", validators=[InputRequired("Please enter a Password"), EqualTo("reTypePassword", "Passwords must match")]
    ,render_kw={"icon": "vpn_key", "required": False, "helperText": "Word a phrase to keep secret", "type": "password"})


    reTypePassword = PasswordField("Re-Type Password", validators=[InputRequired("Please re-type your password")]
    ,render_kw={"icon": "vpn_key", "required": False, "helperText": "Re type the above field", "type": "password"})
