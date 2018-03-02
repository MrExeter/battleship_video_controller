'''
Description - Video Kiosk Model
@author - John Sentz
@date - 01-Mar-2018
@time - 2:21 PM
'''


from app import db
from datetime import datetime


class Kiosk(db.Model):
    __tablename__ = 'kiosk'

    id = db.Column(db.Integer, primary_key=True)
    network_address = db.Column(db.String(36), nullable=False, index=True)
    location = db.Column(db.String(128), nullable=False)

    def __init__(self, network_address, location):
        self.network_address = network_address
        self.location = location

    def __repr__(self):
        return 'Video Controller ip={} at location : {}'.format(self.network_address, self.location)



