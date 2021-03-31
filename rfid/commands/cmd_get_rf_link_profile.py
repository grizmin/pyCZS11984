from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
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

    def __init__(self, cmd="6A", addr=0x01, length=0x03):
        super().__init__(cmd, addr=addr, length=length)

    def _process_result(self, result: bytes) -> bool:
        if result:
            r = self.bytes_to_hex(result)
            profile = int(r[-2], 16)
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
        s = session.write(self.command)
        r = session.read(self.length+4)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
