'''
Description - Development run configuration
@author - John Sentz
@date - 20-Nov-2018
@time - 11:09 AM
'''

DEBUG = True
SERVER_NAME = '127.0.0.1:5000'
localhost = SERVER_NAME
SECRET_KEY = 'applejack'
WTF_CSRF_SECRET_KEY = 'applejack'
CSRF_SESSION_KEY = 'applejack'
# SQLALCHEMY_DATABASE_URI = 'postgresql://dbdeveloper:dbdeveloper@localhost/battleship_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False

