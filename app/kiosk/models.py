'''
Description - Video Kiosk Model
@author - John Sentz
@date - 01-Mar-2018
@time - 2:21 PM
'''

import requests

from app import db


class Kiosk(db.Model):
    """A kiosk represents a single Raspberry PI video display system \
    described by an IP address, location and a node url"""
    __tablename__ = 'kiosk'

    id = db.Column(db.Integer, primary_key=True)
    network_address = db.Column(db.String(36), nullable=False, index=True)
    location = db.Column(db.String(128), nullable=False)
    node_url = db.Column(db.String(128), nullable=False, unique=True)

    def status(self):
        """Method that takes the kiosks assigned ip address and \
        retrieves the current status from the kiosk in JSON format """
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
        # """Method that given an ip address and a location (description) \
        # creates a Kiosk object and saves it to the database"""
        kiosk = cls(network_address=network_address,
                    location=location)

        db.session.add(kiosk)
        db.session.commit()
        return kiosk

    def __init__(self, network_address, location):
        self.network_address = network_address
        self.location = location
        self.node_url = 'http://' + network_address + ':5000/'

    def __repr__(self):
        return 'Video Controller ip={} at location : {}'.format(self.network_address, self.location)


class Scheduler(db.Model):
    """A Scheduler represents an event schedule for either a single or \
    multiple Raspberry PIs."""
    __tablename__ = 'scheduler'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    start_date_time = db.Column(db.DateTime)
    end_date_time = db.Column(db.DateTime)
    default = db.Column(db.Boolean, default=False)
    continuous = db.Column(db.Boolean, default=False)

    def __init__(self, name, description, start_date_time, end_date_time, default, continuous):
        self.name = name
        self.description = description
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.default = default
        self.continuous = continuous

    @classmethod
    def create_scheduler(cls, name, description, start_date_time, end_date_time, default, continuous):
        scheduler = cls(name=name,
                        description=description,
                        start_date_time=start_date_time,
                        end_date_time=end_date_time,
                        default=default,
                        continuous=continuous)

        db.session.add(scheduler)
        db.session.commit()
        return scheduler

    @classmethod
    def delete_scheduler(cls, scheduler):
        db.session.delete(scheduler)
        db.session.commit()
