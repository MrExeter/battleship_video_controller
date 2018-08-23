from celery.schedules import crontab
from celery import Celery


# CELERY_BROKER_URL = 'amqp://localhost//'
# CELERY_BACKEND = 'db+postgresql://dbdeveloper:dbdeveloper@localhost/celery_test_db'

CELERY_BROKER_URL='redis://localhost:6379'
CELERY_RESULT_BACKEND='redis://localhost:6379'

# CELERY_IMPORTS = ('app.kiosk.routes.wake_kiosk',)

CELERY_TIMEZONE = 'US/Pacific'
TIME_ZONE = 'US/Pacific'
USE_TZ = True

wake_url = 'http://10.0.1.13:5100/wake_kiosk_display'
sleep_url = 'http://10.0.1.13:5100/sleep_kiosk_display'

# celery.timezone = timezone

# CELERYBEAT_SCHEDULE = {
#
#     'wake_terminals': {
#         'task': 'app.kiosk.routes.wakeup',
#         # 'schedule': crontab(minute="27",
#         #                     hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
#         #                     day_of_week="*",
#         #                     month_of_year="*"),
#         'schedule': 17,
#         'options': {'queue': 'celery_periodic'}
#     },
#
#     'sleep_terminals': {
#         'task': 'app.kiosk.routes.sleeper',
#         # 'schedule': crontab(minute="50",
#         #                     hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
#         #                     day_of_week="*",
#         #                     month_of_year="*"),
#         'schedule': 37,
#         'options': {'queue': 'celery_periodic'}
#     },
# }




# celery = Celery(__name__, broker=CELERY_BROKER_URL, include=['app.kiosk.routes'])

