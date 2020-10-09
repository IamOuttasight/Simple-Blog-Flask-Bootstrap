from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class RegisterForm(Form):
    name = StringField('Name', validators=[validators.Length(min=1, max=50)])
    username = StringField('Username', validators=[
        validators.Length(min=4, max=25),
        validators.Regexp(r'^[a-zA-Z0-9_-]+$',
            message='Only letters a-z and A-Z, digits and symbols -_ are allowed.')
    ])
    email = EmailField('Email', validators=[
        validators.Length(min=6, max=50),
        validators.Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm password')


class ArticleForm(Form):
    title = StringField('Title', validators=[validators.Length(min=1, max=205)])
    body = TextAreaField('Content', validators=[validators.Length(min=30)])