from celery.schedules import crontab

# CELERY_BROKER_URL = 'amqp://localhost//'
# CELERY_BACKEND = 'db+postgresql://dbdeveloper:dbdeveloper@localhost/celery_test_db'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_IMPORTS = ('app.kiosk.routes',)
ENABLE_UTC = False
CELERY_TIMEZONE = 'US/Pacific'
TIME_ZONE = 'US/Pacific'
USE_TZ = True

# CELERYBEAT_SCHEDULE = {
#
#     'wake_terminals_every_morning': {
#         'task': 'wake_all_kiosks',
#         # 'schedule': crontab(minute="27",
#         #                     hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
#         #                     day_of_week="*",
#         #                     month_of_year="*"),
#         'schedule': crontab(minute="*"),
#     },
#
#     'sleep_terminals_every_morning': {
#         'task': 'qpp.sleep_all_kiosks',
#         'schedule': crontab(minute="33",
#                             hour="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23",
#                             day_of_week="*",
#                             month_of_year="*"),
#     },
# }
