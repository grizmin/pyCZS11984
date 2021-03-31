from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class CMD_set_frequency_user_defined(RFIDCommand):
    """ Command set frequency of CZS6147 controller.
        The baudrate will be written to persistent memory.

        Regions:
        0x01 FCC
        0x02 ETSI
        0x03 CHN
        0x04 user defined

        Freq space:
        frequency space = FreqSpace x 10KHz [default: 50]

        Freq quantity:
        larger than 0. Steps count. [default: 10]

        Freq start:
        865.00 MHz 928.00 MHz (865000 - 928000)

        Example params array:
        region (user)   freq space  freq quantity    freq start
        [4,                50,          10,                865000]
    """
    def __init__(self, frequency_params: List[int]):
        self.freq_params = frequency_params
        super().__init__('78', param_data=self.freq_params)

    @property
    def freq_params(self) -> List[int]:
        """
        Returns: frequency parameter list.
        """
        return self._freq_params

    @freq_params.setter
    def freq_params(self, freq_params: List[int]) -> None:
        assert 4 <= freq_params[0] <= 4, "Spectrum region must be 4 (fixed)"
        assert 0 <= freq_params[1] <= 1000, "Freq space must be in range 0-1000"
        assert 1 <= freq_params[2] <= 1000, "Freq quantity 1-1000"
        assert 865000 <= freq_params[3] <= 928000, "Start frequency"
        self._freq_params = freq_params

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
        r = session.read(self.length+3)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
