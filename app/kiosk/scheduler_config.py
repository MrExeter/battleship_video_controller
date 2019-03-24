'''
Description - Celery Config file and default schedule
@author - John Sentz
@date - 16-Oct-2018
@time - 12:12 PM
'''

"""
Note:  To Debug or test celery functioning, e.g., rapid power on and off of terminal (on then off every 5 minutes)
simply change the crontab times below to match the current hour and next, remember to comment this out and go
back to the default schedule
"""

from app import celery
from celery.schedules import crontab


celery.conf.enable_utc = False
celery.conf.timezone = 'US/Pacific'
celery.conf.beat_schedule = {
    'wake_terminals_every_morning': {
        'task': 'app.kiosk.routes.wake_all_kiosks',
        'schedule': crontab(hour=9, minute=50, day_of_week='*', month_of_year='*'),
        # 'schedule': crontab(hour=[14, 15], minute=[0, 10, 20, 30, 40, 50]),
    },


    'sleep_terminals_every_afternoon': {
        'task': 'app.kiosk.routes.sleep_all_kiosks',
        'schedule': crontab(hour=17, minute=0, day_of_week='*', month_of_year='*'),
        # 'schedule': crontab(hour=[14, 15], minute=[5, 15, 25, 35, 45, 55]),
    },
}
