from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial
from typing import Callable
from time import sleep
from . constants import ERR_CODES

class cmd_set_reader_address(RFIDCommand):
    """ Command get reader address of CZS6147 controller.
    """

    default_timeout = 0.1

    def __init__(self, addr: int):
        """

        Args:
            addr: controller address in the range 0-255
        """
        self.address = addr
        super().__init__('73', param_data=[self.address])

    @property
    def address(self) -> int:
        """

        Returns: controller address

        """
        return self._address

    @address.setter
    def address(self, addr: int) -> None:
        assert 0 <= addr <= 255, "address must be in rage 0-255"
        self._address = addr

    def _process_result(self, result: bytes) -> bool:
        r = self._parse_result(result)[-1][-2]
        return ERR_CODES[f'0x{r}'][1]

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            callback: callback result processor
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
