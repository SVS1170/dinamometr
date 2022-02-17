import struct
import time
import serial
address = 85
port = "com10"

class Dinamometr:
    def __init__(self, address, port):
        self.addr = struct.pack('B', address)
        self.port1 = port

    def open_port(self, port1):
        ser = serial.Serial(f"{port1}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        return ser

    def crc16(self, data):
        crc = 0xFFFF
        l = len(data)
        i = 0
        while i < l:
            j = 0
            crc = crc ^ data[i]
            while j < 8:
                if (crc & 0x1):
                    mask = 0xA001
                else:
                    mask = 0x00
                crc = ((crc >> 1) & 0x7FFF) ^ mask
                j += 1
            i += 1
        if crc < 0:
            crc -= 256
        result = data + chr(crc % 256).encode('latin-1') + chr(crc // 256).encode('latin-1')
        return result

    def zapros(self):
        chunk = self.addr
        chunk += b'\x55'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        dat = ser.read_all()
        zdat = list(dat)
        lengzdat = len(zdat)
        a1 = zdat[lengzdat - 3]             #отсекаем контрольную сумму
        return a1

din = Dinamometr(address, port)
print(din.zapros())