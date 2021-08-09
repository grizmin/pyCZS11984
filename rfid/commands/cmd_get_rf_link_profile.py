from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_get_rf_link_profile(RFIDCommand):
    """ Command rf link profile of CZS6147 controller.
        ProfileID
        0xD0
            Profile 0: Tari 25uS,FM0 40KHz.
        0xD1
            Profile 1: Tari 25uS, Miller 4 250KHz.
                Profile 1 is the recommended and default setting.
        0xD2
            Profile 2: Tari 25uS,Miller 4 300KHz.
        0xD3
            Profile 3: Tari 6.25uS,FM0 400KHz.
    """
    default_timeout = 0.1

    def __init__(self, cmd="6A"):
        super().__init__(cmd)

    def _process_result(self, result: bytes) -> bool:
        if result:
            result = self._parse_result(result)[-1]
            profile = int(result[-2], 16)
            return {'profile': profile}
        return 'Command returned nothing.'

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
