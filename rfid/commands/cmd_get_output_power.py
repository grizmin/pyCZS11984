from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from serial import Serial
from time import sleep


class cmd_get_output_power(RFIDCommand):
    """ Command get output power of CZS6147 controller.
    """
    default_timeout = 0.1

    def __init__(self):
        super().__init__('77')

    def _process_result(self, result: bytes) -> bool:
        result = self._parse_result(result)[-1]
        r = result[-2]
        out_data = {"power": int(r, 16)}
        return out_data

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
