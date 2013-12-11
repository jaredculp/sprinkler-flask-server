import Adafruit_BBIO.UART as UART
import serial
import logging
import random
log = logging.getLogger('werkzeug')

UART.setup("UART1")
UART.setup("UART2")
UART.setup("UART4")
UART.setup("UART5")

def generate_raw_input(sprinkler, opcode, ser):
    on_off = False 
    if opcode == 0: # turn on
        on_off = 1	
    elif opcode == 1: # turn off
        on_off = 0
    elif opcode == 2: # maintain
        if sprinkler.status.lower() == "on":
            on_off = 1
    else:
        on_off = 0
    m1 = chr((0 << 7) | (sprinkler.id << 2) | (on_off << 1) | 0)
    if ser:
        ser.flushInput()
        moisture = ser.read(1)
        m3 = chr((0 << 7) | (int(100 - ord(moisture)/2.55)))
    else:
        m3 = chr((0 << 7) | (random.randint(0, 128)))
    m2 = chr((0 << 7) | (random.randint(0, 128)))
    generated = {'m1': m1, 'm2': m2, 'm3': m3}
    return generated

def communicate(sprinkler, action):
    try:
        ser = serial.Serial(port=sprinkler.uart, baudrate=9600, timeout=None)
    except:
        ser = False
    if action.lower() == "on":
        opcode = 0
    elif action.lower() == "off":
        opcode = 1
    elif action.lower() == "status":
        opcode = 2
    else:
        opcode = 3

    out = OutgoingMessage(1, sprinkler.id, opcode)
    log.warning(out)
    out.send_message(ser) #sent message, wait for ACK

    if ser:
        ser.flushInput()
        m1 = ser.read(1)
        m2 = ser.read(1)
        m3 = ser.read(1)
    else:
        input = generate_raw_input(sprinkler, opcode, ser)
        m1 = input.get('m1')
        m2 = input.get('m2')
        m3 = input.get('m3')

    incoming = IncomingMessage(m1, m2, m3)
    log.warning(incoming)
    incoming.from_binary()
    if ser:
        ser.close()
    return incoming

class OutgoingMessage():

    def __init__(self, master, address, opcode):
        self.master = master
        self.address = address
        self.opcode = opcode
        self.raw = False

    def __repr__(self):
        return '<OutgoingMessage: master=%r, address=%r, opcode=%r, raw=%r>' % (self.master, self.address, self.opcode, self.raw)

    def to_binary(self):
        self.raw = chr((self.master << 7) | (self.address << 2) | (self.opcode))

    def send_message(self, ser):
        self.to_binary()
        if ser:
            ser.flush()
        if ser:
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
        return '<IncomingMessage: master=%r, address=%r, status=%r, error=%r, flow=%r, moisture=%r>' % (self.master1, self.address, self.status, self.error, self.flow, self.moisture)

    def from_binary(self):
        self.master1 = ord(self.raw1) >> 7 
        self.address = (ord(self.raw1) >> 2) & 0x1F
        self.status = (ord(self.raw1) >> 1) & 0x1
        self.error = ord(self.raw1) & 0x1

        self.master2 = ord(self.raw2) >> 7 
        self.flow = ord(self.raw2) & 0x7f

        self.master3 = ord(self.raw3) >> 7
        self.moisture = ord(self.raw3) & 0x7f
