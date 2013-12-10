from app import db
from message import communicate, OutgoingMessage, IncomingMessage

import logging
log = logging.getLogger('werkzeug')

class SprinklerPowerError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Sprinkler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    status = db.Column(db.String(25))
    flow = db.Column(db.Integer)
    moisture = db.Column(db.Integer)
    uart = db.Column(db.String(25))

    def __init__(self, name, status, flow, moisture, uart):
        self.name = name
        self.status = status
        self.flow = flow
        self.moisture = moisture
        self.uart = uart 

    def __repr__(self):
        return '<Sprinkler#%r %r, Status=%r>' % (self.id, self.name, self.status)

    def process_request(self, response):
        log.warning(response)
        if response.status: # status = 1
            self.status = "ON"
        else:
            self.status = "OFF"

        if response.flow:
            self.flow = response.flow
        if response.moisture:
            self.moisture = response.moisture

    def turn_on(self):
        self.process_request(communicate(self, 'ON'))
        if self.status == "OFF":
            raise SprinklerPowerError("Failed to turn sprinkler ON")
        else:
            db.session.commit()

    def turn_off(self):
        self.process_request(communicate(self, 'OFF'))
        if self.status == "ON":
            raise SprinklerPowerError("Failed to turn sprinkler OFF")
        else:
            db.session.commit()

    def get_status(self):
        self.process_request(communicate(self, 'STATUS'))
        db.session.commit()
