from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class cmd_get_rf_port_return_loss(RFIDCommand):
    """
    Command return for the working frequency.
        Return loss value , the unit is dB.
        VSWR = (10^(RL/20) + 1)/(10^(RL/20) -1)
    """

    def __init__(self, cmd="7E", addr=0x01, length=0x03):
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
