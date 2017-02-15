from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class RegisterForm(Form): #creates fields from 
    fullname = StringField("Full Name", [validators.required()])
    email = EmailField("Email", [validators.required()])
    username = StringField("User Name", [
        validators.required(),
        validators.length(min=4,max=25)
        ])
    password = PasswordField("New Password", [
        validators.required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=4, max=80)
        ])
    confirm = PasswordField("Confirm Password")
    
class LoginForm(Form):
    username = StringField("Username", [
        validators.Required(),
        validators.Length(min=4,max=25)
        ])
    password = PasswordField("Password", [
        validators.Required(),
        validators.Length(min=4, max=80)
        ])