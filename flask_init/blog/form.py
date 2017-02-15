from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.fields.html5 import EmailField
from author.form import RegisterForm

class SetupForm(RegisterForm): 
    name = StringField('Blog Name', [
        validators.Required(),
        validators.Length(max=80)
        ])
    