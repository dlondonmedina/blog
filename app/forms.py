from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class NewEntryForm(FlaskForm):
   post_title = StringField('Title', validators=[DataRequired()])
   slug = StringField('Slug', validators=[DataRequired()])
   text = TextAreaField('Text', validators=[DataRequired()])
   submit = SubmitField('Submit')


class LoginForm(FlaskForm):
   email = StringField('Email', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
   remember_me = BooleanField('Remember Me')
   submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
   username = StringField('Username', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired(), Email()])
   first = StringField('First Name', validators=[DataRequired()])
   last = StringField('Last Name', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
   password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Register!')

   def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
         raise ValidationError('User already exists.')

   def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
         raise ValidationError('User already exists.')
