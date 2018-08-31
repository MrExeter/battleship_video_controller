'''
Description - Video Kiosk Forms
@author - John Sentz
@date - 01-Mar-2018
@time - 2:29 PM
'''

import re

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import TimeField

from app.kiosk.models import Kiosk, Scheduler


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


def schedule_name_exists(form, field):
    scheduler = Scheduler.query.filter_by(name=field.data).first()

    if scheduler:
        raise ValidationError('A scheduler by that name already exists')


def edit_schedule_name_exists(args, field):
    temp_name = session["current_scheduler_name"]   # Retrieve session variable for kiosk ip address
    scheduler = Scheduler.query.filter_by(name=field.data).first()

    if not scheduler:
        return True

    name = scheduler.name
    if name == temp_name:
        session["current_scheduler_name"] = ''
        return True

    if scheduler:
        raise ValidationError('A scheduler by that name already exists')


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


class CreateSchedulerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           schedule_name_exists])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start time', format='%H:%M')
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('End time', format='%H:%M')
    # start_date_time = DateTimeField('Start', format='%Y-%m-%d::%H:%M:%S')
    # end_date_time = DateTimeField('Enders', format='%m/%d/%y')
    # start_date_time = DateTimeField("Start",
    #                                 format="%Y-%m-%d :: %H:%M:%S",
    #                                 default=datetime.datetime.now())
    # start_date_time = DateTimeField(label='Start time',
    #                                 format="%d-%b-%Y -- %H:%M", default=datetime.datetime.now())
    #
    # end_date_time = DateTimeField(label='End time',
    #                               format="%d-%b-%Y -- %H:%M", default=datetime.datetime.now())

    default = BooleanField('Default')
    continuous = BooleanField('Continuous')

    submit = SubmitField('Create Schedule')


class EditSchedulerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),
                                           edit_schedule_name_exists])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    start_time = TimeField('Start time', format='%H:%M')
    end_date = DateField('End Date', format='%Y-%m-%d')
    end_time = TimeField('End time', format='%H:%M')
    default = BooleanField('Default')
    continuous = BooleanField('Continuous')

    submit = SubmitField('Update Schedule')
