'''
Description - Video Kiosk Forms
@author - John Sentz
@date - 01-Mar-2018
@time - 2:29 PM
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateKioskForm(FlaskForm):

    network_address = StringField('Network Address', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditKioskForm(FlaskForm):

    network_address = StringField('Network Address', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update')

