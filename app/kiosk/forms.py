'''
Description - Video Kiosk Forms
@author - John Sentz
@date - 01-Mar-2018
@time - 2:29 PM
'''

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

from app.kiosk.models import Kiosk


def edit_network_address_exists(form, field):
    # Check to see if IP address is already being used
    temp_address = session["current_address"]   # Retrieve session variable for kiosk ip address
    kiosk = Kiosk.query.filter_by(network_address=field.data).first()

    if not kiosk:
        return True

    network_address = kiosk.network_address
    if network_address == temp_address:
        session["current_address"] = ''
        return True

    if kiosk:
        raise ValidationError('IP address already in use')


def network_address_exists(form, field):
    # Check to see if IP address is already being used
    kiosk = Kiosk.query.filter_by(network_address=field.data).first()

    if kiosk:
        raise ValidationError('IP address already in use')


def network_address_valid(form, field):
    # Check to see if IP address is in valid form e.g., ###.###.###.### where each ### is 255 or less
    valid_ip_pattern = re.compile(
        "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    test = valid_ip_pattern.match(field.data)
    if not test:
        raise ValidationError('Invalid IP address format')


class CreateKioskForm(FlaskForm):
    network_address = StringField('Network Address', validators=[DataRequired(),
                                                                 network_address_exists,
                                                                 network_address_valid])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create')


class EditKioskForm(FlaskForm):
    network_address = StringField('Network Address', validators=[DataRequired(),
                                                                 edit_network_address_exists,
                                                                 network_address_valid])

    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update')

    def address_unchanged(self, address):
        pass
