from app import db
from message import serial_init, communicate, OutgoingMessage, IncomingMessage

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

    def __init__(self, name, status, flow, moisture):
        self.name = name
        self.status = status
        self.flow = flow
        self.moisture = moisture

    def __repr__(self):
        return '<Sprinkler#%r %r, Status=%r>' % (self.id, self.name, self.status)

    def process_request(self, response):
        if response.status: # status = 1
            self.status = "ON"
        else:
            self.status = "OFF"

        if response.flow:
            self.flow = response.flow
        if response.moisture:
            self.moisture = response.moisture

    def turn_on(self):
        self.process_request(communicate(self.id, 'ON'))
        if self.status == "OFF":
            raise SprinklerPowerError("Failed to turn sprinkler %r ON" % self.id)
        else:
            db.session.commit()

    def turn_off(self):
        self.process_request(communicate(self.id, 'OFF'))
        if self.status == "ON":
            raise SprinklerPowerError("Failed to turn sprinkler %r OFF" % self.id)
        else:
            db.session.commit()

    def get_status(self):
        self.process_request(communicate(self.id, 'STATUS'))
        db.session.commit()
