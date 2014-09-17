import serial
import threading
from time import sleep
from enum import Enum, unique  
from safe_print import safe_print

@unique 
class PacketType(Enum):
    UNDEFINED = 0x00
    storage_availability = 0x01
    supply_availability = 0x02
    radiation_alert = 0x03
    stop = 0x04
    resume = 0x05
    status = 0x06
    heartbeat = 0x07
    # Types 0x10 and higher are user defined
    protocol_message = 0x10
    message = 0x11
    value = 0x12
    
class PacketValidityError(Exception):
   pass

class Packet:
    me = 0
    bot = 18
    
    """
    A packet of data
    """
    def __init__(self, pkt_type, data=None, source=me, destination=bot, length=None, valid=True):
        self.type = pkt_type
        self.length = length
        self.source = source
        self.destination = destination
        self.data = data
        self.valid = valid
        
    def __str__(self):
        return ("Valid" if self.valid else "Invalid") + \
            " packet of type %s sent from %d to %d with data %s" % \
            (self.type, self.source, self.destination, repr(self.data))
    
    def calculate_length(self):
        length = 5
        if self.type == PacketType.storage_availability or self.type == PacketType.supply_availability:
            length += 1
        elif self.data != None:
            length += len(self.data)
        return length
        
    @staticmethod
    def checksum(length, bytes):
        checksum = length
        
        for byte in bytes: 
            try:
                checksum += ord(byte)
            except TypeError:
                checksum += byte
            
            # Mimic 8-bit integer overflow
            if checksum > 0xFF: checksum -= 0xFF;
        
        return 0xFF - checksum
    
    @staticmethod
    def from_data(length, raw_data):
        """ Raw data is the message type through the checksum """
        # Packet type is the first byte in raw_data
        try:
            pkt_type = PacketType( ord(raw_data[0]) )
        except ValueError:
            pkt_type = PacketType.UNDEFINED
        
        length = length
        
        # Source address is the second byte
        source = ord(raw_data[1])
        # And destination is the third
        destination = ord(raw_data[2])
        
        # Data is the third through next-to-last bytes
        data = raw_data[3:-1]
        
        # Check validity on bytes 0 through len-1 
        chk = Packet.checksum(length, raw_data[0:-2])
        valid = chk == ord(raw_data[-1])
        
        return Packet(pkt_type, data, source=source, destination=destination, length=length, valid=valid)
    
    def to_data(self):
        if not self.valid:
            raise PacketValidityError("Attempted to send invalid packet")
        # Start with 0x5F
        data = bytearray([0x5F])
        
        # Then add length
        l = self.length if self.length is not None else self.calculate_length()
        if (l > 255):
            raise PacketValidityError("Attempted to send packet of more than 255 bytes") 
        data.append(l)
        
        # Then add type
        data.append(self.type.value)
        
        # Then add source
        data.append(self.source)
        
        # Then add destination
        data.append(self.destination)
        
        # Then add data
        if self.data != None:
            data.append(self.data)
            
        # And finally, add checksum
        data.append(Packet.checksum(l, data[2:])) # Exclude start byte and length from checksum (length is included but is passed from first argument)
        
        return data
    
    def send(self):
        if (serial_port.isOpen()):
            serial_port.write(self.to_data())
        else:
            safe_print("! Serial connection isn't open")

class BluetoothListener(threading.Thread):
    def __init__(self, func, print_func):
        threading.Thread.__init__(self)
        self.func = func
        self.print_func = print_func
        
    def run(self):
        if not serial_port.isOpen(): connect()
        while True:
            try:
                data = ord(serial_port.read(1)) # Get first byte
                if (data == 0x5F): # 0x5F is the start byte in the reactor protocol
                    length = ord(serial_port.read(1))
                    pkt = Packet.from_data(length, serial_port.read(length-1))
                    self.func(pkt)
                else:
                    self.print_func("Discarded byte 0x%X" % data)
            except serial.SerialException:
                self.print_func("! Serial connection closed. Connect again using 'connect'")
                serial_port.close()
                return # Ends the thread
            

serial_port = serial.Serial()

def connect(which="debug"): 
    print "Connecting..."
    
    serial_port.port = '/dev/tty.BT_18-DevB'
    serial_port.baudrate = 115200
        
    serial_port.timeout = None
    if serial_port.isOpen(): serial_port.close()
    serial_port.open()
    print "Connected"
    
def start(which, func, print_func):
    connect(which)
    listener = BluetoothListener(func, print_func)
    listener.daemon = True
    listener.start()
