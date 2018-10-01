from app import celery
from celery.schedules import crontab


celery.conf.enable_utc = False
celery.conf.timezone = 'US/Pacific'
celery.conf.beat_schedule = {
    'wake_terminals_every_morning': {
        'task': 'app.kiosk.routes.wake_all_kiosks',
        # 'schedule': crontab(hour=9, minute=55, day_of_week='*', month_of_year='*'),
        'schedule': crontab(hour=[15, 16], minute=[0, 10, 20, 30, 40, 50]),
    },


    'sleep_terminals_every_afternoon': {
        'task': 'app.kiosk.routes.sleep_all_kiosks',
        # 'schedule': crontab(hour=17, minute=0, day_of_week='*', month_of_year='*'),
        'schedule': crontab(hour=[15, 16], minute=[5, 15, 25, 35, 45, 55]),
    },
}
