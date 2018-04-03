import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(config_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    csrf.init_app(app)

    app.config.from_pyfile(configuration)

    db.init_app(app)  # bind database to flask app
    bootstrap.init_app(app)  # Initialize Bootstrap

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.kiosk import main  # import blueprint
    app.register_blueprint(main)  # register blueprint

    from app.auth import authentication  # import authentication
    app.register_blueprint(authentication)  # register authentication

    return app
