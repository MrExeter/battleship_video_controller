'''
Description - Scheduler Forms
@author - John Sentz
@date - 25-Jun-2018
@time - 3:58 PM
'''

from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, ValidationError
import re

from app.scheduler.models import Scheduler


class CreateSchedulerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date_time = DateTimeField('Start')
    end_date_time = DateTimeField('End')
    repeat = BooleanField('Repeat')


class EditSchedulerForm(FlaskForm):
    pass
