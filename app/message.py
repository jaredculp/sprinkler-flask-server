import serial

def serial_init():
	ser = serial.Serial(timeout=1)
	ser.baudrate = 9600
	ser.port = 0
	ser.open()
	return ser

def communicate(address, action):
	ser = serial_init()

	if action.lower() == "on":
		opcode = 0
	elif action.lower() == "off":
		opcode = 1
	elif action.lower() == "status":
		opcode = 2
	else:
		opcode = 3

	out = OutgoingMessage(1, address, opcode)
	out.send_message(ser) #sent message, wait for ACK

	##waiting assumably

	m1 = ser.read()
	m2 = ser.read()
	m3 = ser.read()

	incoming = IncomingMessage(m1, m2, m3)
	incoming.from_binary()
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
		self.raw = bin(self.master << 7) + bin(self.address << 2) + bin(opcode)

	def send_message(self, ser):
		ser.isOpen()
		self.to_binary()
		ser.write(self.raw)

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
		self.master1 = int(self.raw1, 2) & 0x80
		self.address = int(self.raw1, 2) & 0x7c
		self.status = int(self.raw1, 2) & 0x2
		self.error = int(self.raw1, 2) & 0x1

		self.master2 = int(self.raw2, 2) & 0x80
		self.flow = int(self.raw2, 2) & 0x7f

		self.master3 = int(self.raw3, 2) & 0x80
		self.flow = int(self.raw3, 2) & 0x7f




