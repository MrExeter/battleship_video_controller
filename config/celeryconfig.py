from celery.schedules import crontab
from celery import Celery

CELERY_BROKER_URL = 'amqp://localhost//'
CELERY_BACKEND = 'db+postgresql://dbdeveloper:dbdeveloper@localhost/celery_test_db'

CELERY_IMPORTS = ('app.kiosk.routes')

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_TIMEZONE = 'US/Pacific'
TIME_ZONE = 'US/Pacific'
USE_TZ = True

wake_url = 'http://10.0.1.13:5100/wake_kiosk_display'
sleep_url = 'http://10.0.1.13:5100/sleep_kiosk_display'

# celery = Celery(__name__, broker=CELERY_BROKER_URL, include=['app.kiosk.routes'])

CELERYBEAT_SCHEDULE = {

    'wake_terminals_every_morning': {
        'task': 'qpp.kiosk.routes.wake_kiosk',
        # 'schedule': crontab(minute="27",
        #                     hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
        #                     day_of_week="*",
        #                     month_of_year="*"),
        'schedule': crontab(minute="*"),
        'args': wake_url
    },

    'sleep_terminals_every_morning': {
        'task': 'qpp.kiosk.routes.sleep_kiosk',
        'schedule': crontab(minute="33",
                            hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
                            day_of_week="*",
                            month_of_year="*"),
        'args': sleep_url
    },
}
dummy = 1


