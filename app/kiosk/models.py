'''
Description - Video Kiosk Model
@author - John Sentz
@date - 01-Mar-2018
@time - 2:21 PM
'''

from app import db
from sqlalchemy.dialects import postgresql
from datetime import datetime


class Kiosk(db.Model):
    __tablename__ = 'kiosk'

    id = db.Column(db.Integer, primary_key=True)
    network_address = db.Column(db.String(36), nullable=False, index=True)
    location = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(16))
    cpu_stats = db.Column(db.JSON)
    mem_stats = db.Column(db.JSON)
    hdd_stats = db.Column(db.JSON)

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

    def __repr__(self):
        return 'Video Controller ip={} at location : {}'.format(self.network_address, self.location)
