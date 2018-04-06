'''
Description - Video Kiosk Model
@author - John Sentz
@date - 01-Mar-2018
@time - 2:21 PM
'''

from app import db
from sqlalchemy.dialects import postgresql
from datetime import datetime
import requests


class Kiosk(db.Model):
    __tablename__ = 'kiosk'

    id = db.Column(db.Integer, primary_key=True)
    network_address = db.Column(db.String(36), nullable=False, index=True)
    location = db.Column(db.String(128), nullable=False)
    node_url = db.Column(db.String(128), nullable=False, unique=True)

    def status(self):
        url = self.node_url + 'system_stats'
        try:
            r = requests.get(url, timeout=0.1)
            json_content = r.json.im_self.content
            data = True     # OKAY
        except:
            data = False    # ERROR Condition
            return data

        return data

    @classmethod
    def create_kiosk(cls, network_address, location):
        kiosk = cls(network_address=network_address,
                    location=location)

        db.session.add(kiosk)
        db.session.commit()
        return kiosk

    def __init__(self, network_address, location):
        self.network_address = network_address
        self.location = location
        self.node_url = 'http://' + network_address + ':5100/'

    def __repr__(self):
        return 'Video Controller ip={} at location : {}'.format(self.network_address, self.location)
