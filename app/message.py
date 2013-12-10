import Adafruit_BBIO.UART as UART
import serial
import logging
log = logging.getLogger('werkzeug')

UART.setup("UART1")
UART.setup("UART2")
UART.setup("UART4")
UART.setup("UART5")

def communicate(sprinkler, action):
    ser = serial.Serial(port=sprinkler.uart, baudrate=9600, timeout=None)
    if action.lower() == "on":
        opcode = 0
    elif action.lower() == "off":
        opcode = 1
    elif action.lower() == "status":
        opcode = 2
    else:
        opcode = 3

    out = OutgoingMessage(1, sprinkler.id, opcode)
    out.send_message(ser) #sent message, wait for ACK

    ##waiting assumably

    m1 = ser.readline() #timeout=None, read(1) means BLOCK until 1 byte recv'd
    m2 = ser.readline() #for each message
    m3 = ser.readline() #wait for all 3, each 1 byte

    log.warning("m1: %r" % m1)
    log.warning("m2: %r" % m2)
    log.warning("m3: %r" % m3)

    incoming = IncomingMessage(m1, m2, m3)
    incoming.from_binary()
    log.warning(incoming)
    ser.close()
    return incoming

class OutgoingMessage():

    def __init__(self, master, address, opcode):
        self.master = master
        self.address = address
        self.opcode = opcode
        self.raw = False

    def __repr__(self):
        return '<OutgoingMessage: master=%r, address=%r, opcode=%r, raw=%r>' % (
                self.master, self.address, self.opcode, self.raw)

    def to_binary(self):
        self.raw = bin((self.master << 7) | (self.address << 2) | (self.opcode))
	log.warning(self.raw)

    def send_message(self, ser):
        self.to_binary()
        num = ser.write(self.raw)

class IncomingMessage():

    def __init__(self, raw1, raw2, raw3):
        self.master1 = False
        self.address = False
        self.raw1 = raw1
        self.status = False
        self.error = False

        self.master2 = False
        self.flow = False
        self.raw2 = raw2

        self.master3 = False
        self.moisture = False
        self.raw3 = raw3

    def __repr__(self):
        return '<IncomingMessage: master=%r, address=%r, status=%r, error=%r>, flow=%r, moisture=%r>' % (
                self.master1, self.address, self.status, self.error, self.flow, self.moisture)

    def from_binary(self):
	log.warning(type(self.raw1))
        self.master1 = int(self.raw1, 16) >> 7 
        self.address = (int(self.raw1, 16) >> 2) & 0x1F
        self.status = (int(self.raw1, 16) >> 1) & 0x1
        self.error = int(self.raw1, 16) & 0x1

        self.master2 = int(self.raw2, 16) >> 7 
        self.flow = int(self.raw2, 16) & 0x7f

        self.master3 = int(self.raw3, 16) >> 7
        self.moisture = int(self.raw3, 16) & 0x7f
