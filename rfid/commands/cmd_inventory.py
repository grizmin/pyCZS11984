from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class cmd_inventory(RFIDCommand):
    """ Command rf link profile of CZS6147 controller.
    Repeat time of inventory round.
        When Repeat = 255, The inventory duration is minimized.
        For example, if the RF field only has one or two tags,
        the inventory duration could be only 30-50 mS,
        this function provides a possibility for fast antenna
        switch applications on multi-ant devices.
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
