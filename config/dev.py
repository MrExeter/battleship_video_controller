DEBUG = True
# SECRET_KEY = 'dbdeveloper'
SERVER_NAME = '127.0.0.1:5000'
SECRET_KEY = 'applejack'
WTF_CSRF_SECRET_KEY = 'applejack'
CSRF_SESSION_KEY = 'applejack'
SQLALCHEMY_DATABASE_URI = 'postgresql://dbdeveloper:dbdeveloper@localhost/battleship_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
