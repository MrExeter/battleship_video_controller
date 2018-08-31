CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_IMPORTS = ('app.kiosk.routes',)
ENABLE_UTC = False

CELERY_TIMEZONE = 'US/Pacific'
TIME_ZONE = 'US/Pacific'
USE_TZ = True
