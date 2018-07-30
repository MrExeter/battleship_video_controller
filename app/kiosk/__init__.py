
from flask import Blueprint


main = Blueprint('main', __name__, template_folder='templates')

from app.kiosk import routes

existing_address = ''

