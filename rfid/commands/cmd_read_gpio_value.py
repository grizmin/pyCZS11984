from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_read_gpio_value(RFIDCommand):
    """ Command read gpio status of CZS6147 controller.
    """
    default_timeout = 0.1

    def __init__(self):
        super().__init__('60')

    def _process_result(self, result: bytes) -> bool:
        result = self._parse_result(result)[-1]
        print(result)
        gpio1 = int(result[-3], 16)
        gpio2 = int(result[-2], 16)
        return {'gpio1': gpio1, 'gpio2': gpio2}

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
