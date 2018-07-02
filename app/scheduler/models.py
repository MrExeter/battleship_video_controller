'''
Description - Scheduler model -- Sets start and stop times for when a video or playlist plays on a kiosk
@author - John Sentz
@date - 24-Jun-2018
@time - 6:45 PM
'''

from app import db


class Scheduler(db.Model):
    __tablename__ = 'scheduler'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(512))
    start_date_time = db.Column(db.DateTime())
    end_date_time = db.Column(db.DateTime())
    repeat = db.Column(db.Boolean(), default=False)

    def __init__(self, name, description, start_date_time, end_date_time, repeat):
        self.name = name
        self.description = description
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.repeat = repeat

    @classmethod
    def create_scheduler(cls, name, description, start_date_time, end_date_time, repeat):
        scheduler = cls(name=name,
                        description=description,
                        start_date_time=start_date_time,
                        end_date_time=end_date_time,
                        repeat=repeat)


