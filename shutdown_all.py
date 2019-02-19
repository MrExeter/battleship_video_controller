'''
Description - Shutdown class and script for shutting down all processes in the starter script
@author - John Sentz
@date - 02-Oct-2018
@time - 9:47 PM
'''

import sys
import os
import subprocess
from time import sleep

from config.process_commands import *


class APIShutdown:

    def __init__(self):
        pass

    @classmethod
    def shutdown_all(cls):

        #######################################################################
        # Shutdown Flask
        cls.shutdown_flask()
        sleep(5)

        #######################################################################
        # Shutdown Celery (both the beat and the workers)
        cls.shutdown_celery()
        sleep(10)

        #######################################################################
        # Shutdown Redis
        cls.shutdown_redis()
        sleep(5)

        #######################################################################
        # Shutdown RabbitMQ
        cls.shutdown_rabbit_mq()
        sleep(5)

    @classmethod
    def shutdown_flask(cls):
        try:
            flask_status = subprocess.check_output(FLASK_APP_STATUS_CMD, shell=True).split()
            print("Flask being shutdown......")
            ###################################################################
            # Kill pids associated with Flask server
            #
            os.system('kill -9 {}'.format(flask_status[10]))
            os.system('kill -9 {}'.format(flask_status[20]))

        except subprocess.CalledProcessError:
            print("Flask not running......")

    @classmethod
    def shutdown_celery(cls):

        pid_file = "celerybeat.pid"
        try:
            file = open(pid_file, "r")
            for line in file:
                the_pid = line
                os.system('kill {}'.format(the_pid))
            print("Kill Celery Beat")

            # process = subprocess.Popen(CELERY_KILL_ALL_CMD)
            os.system(CELERY_KILL_ALL_CMD)

            # print(process)
            # pid = process.pid
            debug = 1
        except:
            print("Celery not running.....")

    @classmethod
    def shutdown_redis(cls):
        ###################################################################
        # Determine platform e.g. Mac or Linux
        #
        platform = str(sys.platform)

        if platform == 'darwin':
            ###################################################################
            # Running on MAC
            cls.redis_shutdown_mac()

        elif platform.__contains__('linux'):
            ###################################################################
            # Running on LINUX
            cls.redis_shutdown_linux()

        else:
            print('Unknown OS : {}'.format(platform))

    @classmethod
    def shutdown_rabbit_mq(cls):
        ###################################################################
        # Determine platform e.g. Mac or Linux
        #
        platform = str(sys.platform)

        if platform == 'darwin':
            ###################################################################
            # Running on MAC
            cls.rabbitmq_shutdown_mac()

        elif platform.__contains__('linux'):
            ###################################################################
            # Running on LINUX
            cls.rabbitmq_shutdown_linux()

        else:
            print('Unknown OS : {}'.format(platform))

    @classmethod
    def redis_shutdown_mac(cls):

        import redis
        rs = redis.Redis("localhost")
        try:
            response = rs.client_list()
            subprocess.Popen(REDIS_SHUTDOWN_CMD_MAC)
            print("Redis-Server being shut down")
        except:
            # Redis not running
            print("Redis-Server not running")

    @classmethod
    def redis_shutdown_linux(cls):
        try:
            os.system(REDIS_STOP_LINUX)
            print("Shutting down Redis....")
        except:
            print("Redis not running....")

    @classmethod
    def rabbitmq_shutdown_mac(cls):
        try:
            status = subprocess.check_output(RABBITMQ_MAC_SHUTDOWN_CMD)
            print("Shutting down RabbitMQ.....")
        except:
            print("RabbitMQ not running.....")

    @classmethod
    def rabbitmq_shutdown_linux(cls):
        try:
            os.system(RABBITMQ_LINUX_STOP)
            print("Shutting down RabbitMQ....")
        except:
            print("RabbitMQ not running....")


APIShutdown.shutdown_all()
