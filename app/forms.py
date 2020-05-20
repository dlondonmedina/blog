from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewEntryForm(FlaskForm):
   post_title = StringField('Title', validators=[DataRequired()])
   author = StringField('Author', validators=[DataRequired()])
   text = TextAreaField('Text', validators=[DataRequired()])
   submit = SubmitField('Submit')

