from rfid.commands.factory.rfid_command import RFIDCommand
from .constants import ERR_CODES
from typing import Callable
from serial import Serial
from time import sleep


class cmd_set_uart_baudrate(RFIDCommand):
    """ Command set_uart_baudrate of CZS6147 controller.
        The baudrate will be written to persistent memory.
    """
    default_timeout = 0.1

    def __init__(self, baudrate: int):
        self.baudrate = baudrate
        super().__init__('71', param_data=[self.baudrate])

    @property
    def baudrate(self) -> int:
        """

        Returns: active antenna id.

        """
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate: int):
        """
        Maps baudrate to option parameter (CZS6147)
        Args:
            baudrate:
              Serial port baud rate
        Returns:
              parameter according to CZS647 rfc
        """
        br = {115200: 0x04, 38400: 0x03}[baudrate]
        self._baudrate = br


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
