from rfid.commands.factory.rfid_command import RFIDCommand
from .constants import ERR_CODES
from typing import Callable
from serial import Serial
from time import sleep

class cmd_set_work_antenna(RFIDCommand):
    """ Command set_uart_baudrate of CZS6147 controller.
        The baudrate will be written to persistent memory.
    """
    default_timeout = 0.1

    def __init__(self, antenna_id: int):
        self.antenna = antenna_id
        super().__init__('74', param_data=[self.antenna])

    @property
    def antenna(self) -> int:
        """

        Returns: active antenna id.

        """
        return self._antenna_id

    @antenna.setter
    def antenna(self, antenna_id: int) -> None:
        assert 0 <= antenna_id <= 3, "antenna id must be in rage 1-4"
        self._antenna_id = antenna_id

    def _process_result(self, result: bytes) -> bool:
        r = self.bytes_to_hex(result)[-2]
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
