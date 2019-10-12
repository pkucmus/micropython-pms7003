import ustruct as struct
from utime import sleep_ms

class IncorrectData(Exception):
    pass

class PassivePMS7003:
    # https://github.com/teusH/MySense/blob/master/docs/pms7003.md
    # https://patchwork.ozlabs.org/cover/1039261/
    # https://joshefin.xyz/air-quality-with-raspberrypi-pms7003-and-java/
    ENTER_PASSIVE_MODE_REQ = [0x42, 0x4d, 0xe1, 0x00, 0x00, 0x01, 0x70]
    ENTER_PASSIVE_MODE_RES = [0x42, 0x4D, 0x00, 0x04, 0xE1, 0x00, 0x01, 0x74]
    SLEEP_REQ = [0x42, 0x4d, 0xe4, 0x00, 0x00, 0x01, 0x73]
    SLEEP_RES = [0x42, 0x4D, 0x00, 0x04, 0xE4, 0x00, 0x01, 0x77]
    WAKEUP_REQ = [0x42, 0x4d, 0xe4, 0x00, 0x01, 0x01, 0x74]     # NO response
    READ_IN_PASSIVE_REQ = [0x42, 0x4d, 0xe2, 0x00, 0x00, 0x01, 0x71]  # data as response

    def __init__(self, uart):
        self.uart = uart
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self._sendCmd(self.ENTER_PASSIVE_MODE_REQ, self.ENTER_PASSIVE_MODE_RES)

    def _sendCmd(self, req, res):
        for i in req:
            self.uart.writechar(i)
        if res:
            read_buffer = self.uart.read(len(res))
            print(''.join('{:02x}'.format(x) for x in read_buffer))

    def sleep(self):
        self._sendCmd(self.SLEEP_REQ, self.SLEEP_RES)

    def wakeup(self):
        self._sendCmd(self.WAKEUP_REQ, None)

    def read(self):
        self._sendCmd(self.READ_IN_PASSIVE_REQ, None)
        while self.uart.any() < 32:
            sleep_ms(500)
        read_buffer = self.uart.read(32)
        data = struct.unpack('!BBHHHHHHHHHHHHHBBH', read_buffer)
        checksum = 0
        for c in read_buffer[0:30]:
            checksum += c
        if checksum != data[17]:
            raise IncorrectData('bad checksum')
        return data
