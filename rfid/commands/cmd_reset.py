from rfid.commands.factory.rfid_command import RFIDCommand
from .constants import ERR_CODES
from typing import Callable
from serial import Serial
from time import sleep


class cmd_reset(RFIDCommand):

    default_timeout = 0.1
    reset_command = "70"

    def __init__(self):
        super().__init__(cmd=self.reset_command)


    def _process_result(self, result: bytes) -> bool:
        if result:
            r = self._parse_result(result)[-1][-2]
            return ERR_CODES[f'0x{r}'][1]
        # special case - reset command is supposed to return nohing
        return True


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
