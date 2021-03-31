from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class CMD_get_frequency_region(RFIDCommand):
    """ Command set frequency of CZS6147 controller.
        The baudrate will be written to persistent memory.

        Regions:
        0x01 FCC
        0x02 ETSI
        0x03 CHN
        0x04 user defined

        Freq space:
        frequency space = FreqSpace x 10KHz [default: 50]

        Freq quantity:
        larger than 0. Steps count. [default: 10]

        Freq start:
        865.00 MHz 928.00 MHz (865000 - 928000)

        Example response:
        Head|Len|Address|Cmd| Region|FreqSpace|FreqQuantity| Frequency | checksum
        [01|06 | 01    | 79| 04    |    32   |   0A       |  0D 32 E8 |  76     ]
    """
    def __init__(self):
        super().__init__('79')


    def _process_result(self, result: bytes) -> bool:
        # convert to list of hex strings
        result = [f"{v:02x}".upper() for v in result]
        # referring to documentation
        # bytes 8,9,10 - frequency
        freq = int("".join(map(str, result[-4:-1])), 16)
        # byte 7 is frequency space
        freq_space = int(f"{result[-5]}", 16)
        # byte 6 is frequency quantity
        freq_quantity = int(f"{result[-6]}", 16)
        return {"frequency": freq, "freq_space": freq_space, 'freq_quantity': freq_quantity}

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(11)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
