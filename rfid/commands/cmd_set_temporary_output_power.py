from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable
from serial import Serial
from time import sleep
from .constants import ERR_CODES


class cmd_set_temporary_output_power(RFIDCommand):
    """ Command set output power of CZS6147 controller.

    RF output power, range from 20-33(0x14 – 0x21), the unit is dBm.

    This command consumes less than 10uS.
    ★If you want you change the output power frequently, please use this command, which
        doesn’t reduce the life of the internal flash memory.
    """
    default_timeout = 0.1

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
        try:
            r = self._parse_result(result)[-1][-2]
            return ERR_CODES[f'0x{r}'][1]
        except Exception as e:
            if not result:
                print("Device returned nothing. Is this ok?")
            raise e

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
