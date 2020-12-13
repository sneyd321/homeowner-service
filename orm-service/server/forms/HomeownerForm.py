from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class HomeownerForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired(message = "Please enter a first name")], render_kw={"icon": "account_circle"})
    lastName = StringField('Last Name' , render_kw={"icon": "account_circle"})
    email = StringField('Email', render_kw={"icon": "email"})
    phoneNumber = StringField("Phone Number", render_kw={"icon": "smartphone"})
    password = StringField("Password", render_kw={"icon": "vpn_key"})
    reTypePassword = StringField("Re-Type Password", render_kw={"icon": "vpn_key"})


