import os

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_wtf.csrf import CSRFProtect

# from config.dev import CELERY_BROKER_URL
import config.celeryconfig as celeryconfig
# from config.celeryconfig import celery
# from config.celeryconfig import CELERY_BROKER_URL

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'basic'
bcrypt = Bcrypt()

# celery = Celery(__name__, broker=CELERY_BROKER_URL, include=['app.kiosk.routes'])

# import config.celeryconfig as celeryconfig

def create_app(config_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')


    app.config.from_pyfile(configuration)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)  # bind database to flask app
    bootstrap.init_app(app)  # Initialize Bootstrap

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.kiosk import main  # import blueprint
    app.register_blueprint(main)  # register blueprint

    from app.auth import authentication  # import authentication
    app.register_blueprint(authentication)  # register authentication

    # celery = Celery(__name__, broker=CELERY_BROKER_URL, include=['app.kiosk.routes'])

    def make_celery(app):
        # create context tasks in celery
        celery = Celery(__name__, broker=celeryconfig.CELERY_BROKER_URL, include=['app.kiosk.routes'])
        celery.conf.update(app.config)
        celery.config_from_object(celeryconfig)
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

        return celery

    celery = make_celery(app)

    return app
