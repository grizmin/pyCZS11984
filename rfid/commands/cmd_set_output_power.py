from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from time import sleep
from serial import Serial
from . constants import ERR_CODES


class cmd_set_output_power(RFIDCommand):
    """ Command set output power of CZS6147 controller.
        The baudrate will be written to persistent memory.
    """
    default_timeout = 0.1

    def __init__(self, output_power: int):
        self.power = output_power
        super().__init__('76', param_data=[self.power])

    @property
    def power(self) -> int:
        """

        Returns: output power in dBm.

        """
        return self._power

    @power.setter
    def power(self, output_power: int) -> None:
        assert 18 <= output_power <= 26, "Power in dBm must be in range 18-26 (0x12 - 0x1a)"
        self._power = output_power

    def _process_result(self, result: bytes) -> bool:
        r = self._parse_result(result)[-1][-2]
        return ERR_CODES[f'0x{r}'][1]

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
