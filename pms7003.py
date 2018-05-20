import machine
import ustruct as struct


class PMS7003:
    PMS_FRAME_LENGTH = 0
    PMS_PM1_0 = 1
    PMS_PM2_5 = 2
    PMS_PM10_0 = 3
    PMS_PM1_0_ATM = 4
    PMS_PM2_5_ATM = 5
    PMS_PM10_0_ATM = 6
    PMS_PCNT_0_3 = 7
    PMS_PCNT_0_5 = 8
    PMS_PCNT_1_0 = 9
    PMS_PCNT_2_5 = 10
    PMS_PCNT_5_0 = 11
    PMS_PCNT_10_0 = 12
    PMS_VERSION = 13
    PMS_ERROR = 14
    PMS_CHECKSUM = 15

    def get_uart(self):
        uart = machine.UART(2, 9600)
        uart.init(9600, bits=8, parity=None, stop=1)
        return uart

    def _assert_byte(self, byte, expected):
        if byte is None or len(byte) < 1 or ord(byte) != expected:
            return False
        return True

    def read(self):
        uart = self.get_uart()
        while True:
            if not self._assert_byte(uart.read(1), 0x42):
                print('bad first')
                continue
            if not self._assert_byte(uart.read(1), 0x4D):
                print('bad second')
                continue

            read_buffer = uart.read(30)
            if len(read_buffer) < 30:
                continue

            data = struct.unpack('!HHHHHHHHHHHHHBBH', read_buffer)

            checksum = 0x42 + 0x4D
            for c in read_buffer[0:28]:
                checksum += c
            if checksum != data[self.PMS_CHECKSUM]:
                print('bad checksum')
                continue

            return {
                'FRAME_LENGTH': data[self.PMS_FRAME_LENGTH],
                'PM1_0': data[self.PMS_PM1_0],
                'PM2_5': data[self.PMS_PM2_5],
                'PM10_0': data[self.PMS_PM10_0],
                'PM1_0_ATM': data[self.PMS_PM1_0_ATM],
                'PM2_5_ATM': data[self.PMS_PM2_5_ATM],
                'PM10_0_ATM': data[self.PMS_PM10_0_ATM],
                'PCNT_0_3': data[self.PMS_PCNT_0_3],
                'PCNT_0_5': data[self.PMS_PCNT_0_5],
                'PCNT_1_0': data[self.PMS_PCNT_1_0],
                'PCNT_2_5': data[self.PMS_PCNT_2_5],
                'PCNT_5_0': data[self.PMS_PCNT_5_0],
                'PCNT_10_0': data[self.PMS_PCNT_10_0],
                'VERSION': data[self.PMS_VERSION],
                'ERROR': data[self.PMS_ERROR],
                'CHECKSUM': data[self.PMS_CHECKSUM],
            }
