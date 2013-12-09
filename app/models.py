from app import db

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

    def turn_on(self):
        self.status = 'ON'
        db.session.commit()

    def turn_off(self):
        self.status = 'OFF'
        db.session.commit()
