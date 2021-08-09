from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_get_rf_port_return_loss(RFIDCommand):
    """
    Command return for the working frequency.
        Return loss value , the unit is dB.
        VSWR = (10^(RL/20) + 1)/(10^(RL/20) -1)
    """
    default_timeout = 0.1

    def __init__(self, cmd="7E", addr=0x01, length=0x03):
        super().__init__(cmd, addr=addr, length=length)

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
