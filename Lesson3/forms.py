from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username')
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])


class RegistrationForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8),
                                         Regexp('(?=.*[a-z])(?=.*[0-9])',
                                                message="Ошибка! Нужны цифры и буквы!")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    name = StringField('Name')
    surname = StringField('Surname')
    email = StringField('Email', validators=[DataRequired(), Email()])
    #birthday = DateTimeField('Birthday (dd.mm.yyyy)', format='%d.%m.%Y')
    terms = BooleanField("I'm agree with terms conditions and privacy policy.",
                         validators=[DataRequired()])
