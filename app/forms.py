# from xml.dom import ValidationErr
from flask_wtf import FlaskForm
import phonenumbers
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import DateTimeLocalField
from datetime import datetime

from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Come up with your username"})
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your E-mail"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Choose security password"})
    confirm_password = PasswordField('Password', 
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password"})
    remember = BooleanField('I allow access to my location')  #I need to make boolean be required
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your E-mail"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Come up with your username"})
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your E-mail"})
    name = StringField('Name', 
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your name"})
    surname = StringField('Surname', 
                           validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your family name"})
    phoneNumber = StringField('Phone Number', 
                           validators=[DataRequired()], render_kw={"placeholder": "What is your tel. number?"})
    location = StringField('Location', 
                           validators=[DataRequired(), Length(min=2, max=40)], render_kw={"placeholder": "In wich country, city do you live?"})
    languages = StringField('Languages', 
                           validators=[DataRequired(), Length(min=3, max=50)], render_kw={"placeholder": "What languages do you speak?"})
    avatar_picture = FileField(validators=[FileAllowed(['jpg', 'png'])])
    bg_picture = FileField(validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phoneNumber(self, phoneNumber):
        try:
            input_number = phonenumbers.parse(phoneNumber.data)
            if not phonenumbers.is_valid_number(input_number):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class PartyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter a title"})
    date_time = DateTimeLocalField('Event Date', format='%Y-%m-%dT%H:%M', default= datetime.utcnow, render_kw={"placeholder": "When will your party start?"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Where is you party at?"})
    lng = HiddenField('Lng', validators=[DataRequired()])
    lat = HiddenField('Lat', validators=[DataRequired()])
    whatsapp_link = StringField("Chat's link", validators=[DataRequired()], render_kw={"placeholder": "Enter a link for the WhatsApp chat"})
    party_languages = StringField("Languages", validators=[DataRequired()], render_kw={"placeholder": "Choose party's languages"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Enter a description"})
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your E-mail"})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Choose security password"})
    confirm_password = PasswordField('Password', 
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password"})
    submit = SubmitField('Reset Password')