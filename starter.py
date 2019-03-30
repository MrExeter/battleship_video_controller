'''
Description - File and utility class to start flask app, Redis, Celerybeat and Celery workers
@author - John Sentz
@date - 27-Sep-2018
@time - 10:20 PM
'''

import sys
import os
import subprocess
from time import sleep

from config.process_commands import *


class Starter:
    REDIS_PID = None
    CELERY_BEAT_PID = None
    CELERY_WORKER_PID = None

    def __init__(self):
        pass

    @classmethod
    def clean_and_clear(cls):
        pass

    @classmethod
    def start_all(cls):
        ###################################################################
        # Determine platform e.g. Mac or Linux
        #
        platform = str(sys.platform)

        if platform == 'darwin':
            ###################################################################
            # Running on MAC
            #
            print('You are on a MAC : {}'.format(platform))

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
                # os.system(REDIS_MAC_START_CMD)
                subprocess.Popen(REDIS_MAC_START_CMD, shell=True)
                sleep(10)

            ###################################################################
            # Start CeleryBeat if not already running
            #
            cls.start_celery_beat()

            ###################################################################
            # Start Celery-Worker if not already running
            #
            cls.start_celery_worker()

            ###################################################################
            # Start Flask App
            #
            cls.start_flask_app()

        elif platform.__contains__('linux'):
            ###################################################################
            # Running on Linux
            #
            print('You are on Linux : {}'.format(platform))

            ###################################################################
            # Start Redis if not already running
            #
            subprocess.Popen(REDIS_RESTART_LINUX, shell=True)
            sleep(10)

            ###################################################################
            # Start CeleryBeat if not already running
            #
            cls.start_celery_beat()

            ###################################################################
            # Start Celery-Worker if not already running
            #
            cls.start_celery_worker()

            ###################################################################
            # Start Flask App
            #
            cls.start_flask_app()

        else:
            print('Unknown OS : {}'.format(platform))

    @classmethod
    def start_flask_app(cls):
        try:
            flask_status = subprocess.check_output(FLASK_APP_STATUS_CMD, shell=True).split()
            print("Flask already running")
            ###################################################################
            # Kill pids associated with Flask server
            #
            os.system('kill -9 {}'.format(flask_status[10]))
            os.system('kill -9 {}'.format(flask_status[20]))

            ###################################################################
            # Restart Flask
            #
            print("Starting Flask App......")
            process = subprocess.Popen(FLASK_APP_CMD)
            pid = process.pid
            sleep(15)

        except subprocess.CalledProcessError:
            print("Starting Flask App......")
            process = subprocess.Popen(FLASK_APP_CMD)
            pid = process.pid
            sleep(15)

    @classmethod
    def start_celery_worker(cls):
        try:
            status = subprocess.check_output(CELERY_WORKER_STATUS, shell=True)

        except Exception as exp:
            print("Start Celery workers")
            print("Exception :", exp)
            process = subprocess.Popen(CELERY_WORKER_CMD, shell=True)
            pid = process.pid
            sleep(5)

    @classmethod
    def start_celery_beat(cls):
        pid_file = "celerybeat.pid"
        try:
            file = open(pid_file, "r")
            for line in file:
                the_pid = line
                os.system('kill {}'.format(the_pid))
                print("Launching CeleryBeat")
                process = subprocess.Popen(CELERY_BEAT_CMD, shell=True)
                pid = process.pid
                sleep(5)
        except:
            print("Launching CeleryBeat")
            process = subprocess.Popen(CELERY_BEAT_CMD, shell=True)
            pid = process.pid
            sleep(5)

    @classmethod
    def restart_celery_beat(cls):
        # Restart Celery Beat scheduler
        pass


Starter.start_all()
