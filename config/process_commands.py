'''
Description - Commands for starting and shutting down different background services
@author - John Sentz
@date - 02-Oct-2018
@time - 9:50 PM
'''

CELERY_WORKER_CMD = 'celery -A app worker --loglevel=info'
CELERY_BEAT_CMD = 'celery -A app beat'
CELERY_KILL_ALL_CMD = 'sudo pkill -f celery'
CELERY_WORKER_STATUS = 'celery -A app status'
REDIS_MAC_START_CMD = 'redis-server'
REDIS_SERVER_PID = "ps -A | grep -m1 redis-server"
REDIS_SHUTDOWN_CMD_MAC = "redis-cli shutdown"

REDIS_STATUS_LINUX = 'sudo systemctl status redis'
REDIS_START_LINUX = 'sudo systemctl start redis'
REDIS_RESTART_LINUX = 'sudo systemctl restart redis'
REDIS_STOP_LINUX = 'sudo systemctl stop redis'

# RABBITMQ_MAC_RESTART_CMD = 'brew services restart rabbitmq'
# RABBITMQ_MAC_SHUTDOWN_CMD = 'brew services stop rabbitmq'
#
# RABBITMQ_LINUX_STATUS = 'service rabbitmq-server status'
# RABBITMQ_LINUX_START = 'sudo service rabbitmq-server start'
# RABBITMQ_LINUX_STOP = 'sudo service rabbitmq-server stop'
# RABBITMQ_LINUX_RESTART = 'sudo service rabbitmq-server restart'

FLASK_APP_CMD = ["python", "run.py"]
FLASK_APP_STATUS_CMD = 'lsof -i :5000'


