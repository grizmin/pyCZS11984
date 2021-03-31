from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from serial import Serial
from .constants import ERR_CODES


class cmd_set_temporary_output_power(RFIDCommand):
    """ Command set output power of CZS6147 controller.

    RF output power, range from 20-33(0x14 – 0x21), the unit is dBm.

    This command consumes less than 10uS.
    ★If you want you change the output power frequently, please use this command, which
        doesn’t reduce the life of the internal flash memory.
    """
    def __init__(self, rf_power: int):
        self._rf_power = 20   # default value
        self.rf_power = rf_power
        super().__init__('66', param_data=[self.rf_power])

    @property
    def rf_power(self):
        return self._rf_power

    @rf_power.setter
    def rf_power(self, power: int):
        assert 20 <= power <= 33, "RF output power, range from 20-33(0x14 – 0x21), the unit is dBm."

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
        r = session.read(self.length+4)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
