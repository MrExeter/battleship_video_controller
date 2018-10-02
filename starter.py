'''
Description - File and utility class to start flask app, RabbitMQ, Redis, Celerybeat and Celery workers
@author - John Sentz
@date - 27-Sep-2018
@time - 10:20 PM
'''

import sys, os, subprocess
from time import sleep

CELERY_WORKER_CMD = 'celery -A app worker --loglevel=info'
CELERY_BEAT_CMD = 'celery -A app beat'
CELERY_KILL_ALL_CMD = 'sudo pkill -f celery'
CELERY_WORKER_STATUS = 'celery -A app status'
REDIS_START_CMD = 'redis-server'
REDIS_SERVER_PID = "ps -A | grep -m1 redis-server"
REDIS_SHUTDOWN_CMD_MAC = "redis-cli shutdown"

REDIS_STATUS_LINUX = 'sudo systemctl status redis'
REDIS_START_LINUX = 'sudo systemctl start redis'
REDIS_RESTART_LINUX = 'sudo systemctl restart redis'
REDIS_STOP_LINUX = 'sudo systemctl stop redis'

RABBITMQ_MAC_CMD = 'brew services restart rabbitmq'

RABBITMQ_LINUX_STATUS = 'service rabbitmq-server status'
RABBITMQ_LINUX_START = 'sudo service rabbitmq-server start'
RABBITMQ_LINUX_STOP = 'sudo service rabbitmq-server stop'
RABBITMQ_LINUX_RESTART = 'sudo service rabbitmq-server restart'

FLASK_APP_CMD = ["python", "run.py"]
FLASK_APP_STATUS_CMD = 'lsof -i :5000'


class Starter:

    REDIS_PID = None
    RABBITMQ_PID = None
    CELERY_BEAT_PID = None
    CELERY_WORKER_PID = None


    def __init__(self):
        pass

    @classmethod
    def clean_and_clear(cls):

        pass

    @classmethod
    def start_all(cls):
        # Determine platform e.g. Mac or Linux
        platform = str(sys.platform)

        if platform == 'darwin':
            ###################################################################
            # Running on MAC
            #
            print('You are on a MAC : {}'.format(platform))

            ###################################################################
            # Start RabbitMQ if not already running
            #
            # os.system(RABBITMQ_MAC_CMD)
            subprocess.Popen(RABBITMQ_MAC_CMD, shell=True)
            sleep(15)

            ###################################################################
            # Start Redis if not already running
            #
            import redis
            rs = redis.Redis("localhost")
            try:
                response = rs.client_list()
                print("Redis-Server already running")
            except redis.ConnectionError:
                # Redis not running, start
                print("Launching redis server")
                # os.system(REDIS_START_CMD)
                subprocess.Popen(REDIS_START_CMD, shell=True)
                sleep(10)

            ###################################################################
            # Start CeleryBeat if not already running
            #
            pid_file = "celerybeat.pid"
            try:
                file = open(pid_file, "r")
                for line in file:
                    the_pid = line
            except:
                print("Launching CeleryBeat")
                process = subprocess.Popen(CELERY_BEAT_CMD, shell=True)
                pid = process.pid
                sleep(5)

            ###################################################################
            # Start Celery-Worker if not already running
            #
            try:
                status = subprocess.check_output(CELERY_WORKER_STATUS, shell=True)

            except:
                print("Start Celery workers")
                process = subprocess.Popen(CELERY_WORKER_CMD, shell=True)
                pid = process.pid
                sleep(5)
            ###################################################################
            # Start Flask App
            #
            try:
                flask_status = subprocess.check_output(FLASK_APP_STATUS_CMD, shell=True).split()
                print("Flask already running")
                # Kill pids associated with Flask server
                os.system('kill -9 {}'.format(flask_status[10]))
                os.system('kill -9 {}'.format(flask_status[20]))

                # Restart Flask
                sleep(10)
                process = subprocess.Popen(FLASK_APP_CMD).wait()

            except subprocess.CalledProcessError:
                print("Starting Flask App......")

                process = subprocess.Popen(FLASK_APP_CMD).wait()
                pid = process.pid
                sleep(10)

        elif platform.__contains__('linux'):
            print('You are on Linux : {}'.format(platform))

            ###################################################################
            # Start RabbitMQ if not already running
            #
            subprocess.Popen(RABBITMQ_LINUX_RESTART, shell=True)
            sleep(15)

            ###################################################################
            # Start Redis if not already running
            #
            subprocess.Popen(RABBITMQ_LINUX_RESTART, shell=True)
            sleep(10)

            ###################################################################
            # Start CeleryBeat if not already running
            #
            ###################################################################
            # Start CeleryBeat if not already running
            #
            pid_file = "celerybeat.pid"
            try:
                file = open(pid_file, "r")
                for line in file:
                    the_pid = line
            except:
                print("Launching CeleryBeat")
                process = subprocess.Popen(CELERY_BEAT_CMD, shell=True)
                pid = process.pid
                sleep(5)

            ###################################################################
            # Start Celery-Worker if not already running
            #
            try:
                status = subprocess.check_output(CELERY_WORKER_STATUS, shell=True)

            except:
                print("Start Celery workers")
                process = subprocess.Popen(CELERY_WORKER_CMD, shell=True)
                pid = process.pid
                sleep(5)

                ###################################################################
                # Start Flask App
                #
                try:
                    flask_status = subprocess.check_output(FLASK_APP_STATUS_CMD, shell=True).split()
                    print("Flask already running")
                    # Kill pids associated with Flask server
                    os.system('kill -9 {}'.format(flask_status[10]))
                    os.system('kill -9 {}'.format(flask_status[20]))

                    # Restart Flask
                    sleep(10)
                    process = subprocess.Popen(FLASK_APP_CMD).wait()

                except subprocess.CalledProcessError:
                    print("Starting Flask App......")

                    process = subprocess.Popen(FLASK_APP_CMD).wait()
                    pid = process.pid
                    sleep(10)



        else:
            print('Unknown OS : {}'.format(platform))


    @classmethod
    def restart_celery_beat(cls):
        # Restart Celery Beat scheduler
        pass

Starter.start_all()
