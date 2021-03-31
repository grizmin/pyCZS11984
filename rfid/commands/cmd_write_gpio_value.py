from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from . constants import ERR_CODES


class cmd_write_gpio_value(RFIDCommand):
    """ Command set GPIOs of CZS6147 controller.

        valid values:
        0x00 - low
        0x01 - high

        GPIOs:
        0x03 - GPIO3
        0x04 - GPIO4

        Example params argument:
              GPIO   |   value
            [  3     |    1    ]
    """
    def __init__(self, gpio_params: List[int]):
        self.gpio_params = gpio_params
        super().__init__('61', param_data=self._gpio_params)

    @property
    def gpio_params(self) -> List[int]:
        """
        Returns: gpio parameter list.
        """
        return self._gpio_params

    @gpio_params.setter
    def gpio_params(self, gpio_params: List[int]) -> None:
        assert 3 <= gpio_params[0] <= 4, "Choose between GPIO3 and GPIO4"
        assert 0 <= gpio_params[1] <= 1, "Only high (1) or low (0) are allowed"
        self._gpio_params = gpio_params

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
