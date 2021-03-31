from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from serial import Serial


class CMD_set_output_power(RFIDCommand):
    """ Command set output power of CZS6147 controller.
        The baudrate will be written to persistent memory.
    """
    def __init__(self, output_power: int):
        self.power = output_power
        super().__init__('76', param_data=[self._power])

    @property
    def power(self) -> int:
        """

        Returns: output power in dBm.

        """
        return self.output_power

    @power.setter
    def power(self, output_power: int) -> None:
        assert 18 <= output_power <= 26, "Power in dBm must be in range 18-26 (0x12 - 0x1a)"
        self._power = output_power

    def _process_result(self, result: bytes) -> bool:
        r = self.bytes_to_hex(result)[-2]
        return "OK" if r == '10' else "Error"

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        r = session.read(self.length+3)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
