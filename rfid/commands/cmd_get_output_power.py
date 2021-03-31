from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from serial import Serial


class CMD_get_output_power(RFIDCommand):
    """ Command get output power of CZS6147 controller.
    """
    def __init__(self):
        super().__init__('77')

    def _process_result(self, result: bytes) -> bool:
        r = self.bytes_to_hex(result)[-2]
        return f"{int(r, 16)}dBm"

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(self.length+3)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
