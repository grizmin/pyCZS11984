from rfid.commands.factory.rfid_command import RFIDCommand
from .constants import ERR_CODES
from typing import Callable
from serial import Serial


class CMD_reset(RFIDCommand):
    def __init__(self):
        super().__init__('70')

    def _process_result(self, result: bytes) -> bool:
        if result:
            r = self.bytes_to_hex(result)[-2]
            return ERR_CODES[f'0x{r}'][1]
        return 'Controller returned nothing'


    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(self.length+2)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
