from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial
from typing import Callable


class CMD_set_reader_address(RFIDCommand):
    """ Command get reader address of CZS6147 controller.
    """

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
        r = self.bytes_to_hex(result)[-2]
        return r == '10'

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            callback: callback result processor
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(self.length + 4)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)

        return r
