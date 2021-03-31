from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class cmd_read_gpio_value(RFIDCommand):
    """ Command read gpio status of CZS6147 controller.
    """
    def __init__(self):
        super().__init__('60')

    def _process_result(self, result: bytes) -> bool:
        r = self.bytes_to_hex(result)
        gpio1 = int(r[-3], 16)
        gpio2 = int(r[-2], 16)
        return {'gpio1': gpio1, 'gpio2': gpio2}

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(self.length+4)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
