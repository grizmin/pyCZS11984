from rfid.commands.factory.rfid_command import RFIDCommand
from .constants import ERR_CODES
from typing import Callable
from serial import Serial


class CMD_set_uart_baudrate(RFIDCommand):
    """ Command set_uart_baudrate of CZS6147 controller.
        The baudrate will be written to persistent memory.
    """
    def __init__(self, baudrate: int):
        self._baudrate = self.set_baudrate(baudrate)
        super().__init__('71', param_data=[self._baudrate])

    @staticmethod
    def set_baudrate(baudrate: int):
        """
        Maps baudrate to option parameter (CZS6147)
        Args:
            baudrate:
              Serial port baud rate
        Returns:
              parameter according to CZS647 rfc
        """
        br = {115200: 0x04, 38400: 0x03}[baudrate]
        return br

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
        s = session.write(self.command)
        r = session.read(self.length+2)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
