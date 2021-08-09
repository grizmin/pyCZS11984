from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_set_beeper_mode(RFIDCommand):
    """ Command set beeper mode of CZS6147 controller.
        The baudrate will be written to persistent memory.

        modes:
        0x00 Quiet.
        0x01 Beep after every inventory round if tag(s) identified.
        0x02 Beep after every tag has identified.

        Example params array:
        [01]
    """

    default_timeout = 0.1

    def __init__(self, beeper_mode: int):
        self.beeper_mode = beeper_mode
        super().__init__('7A', param_data=[self.beeper_mode])

    @property
    def beeper_mode(self) -> List[int]:
        """
        Returns: frequency parameter list.
        """
        return self._beeper_mode

    @beeper_mode.setter
    def beeper_mode(self, beeper_mode: int) -> None:
        assert 0 <= beeper_mode <= 2, "beeper mode must be in [0, 1, 2]"
        self._beeper_mode = beeper_mode

    def _process_result(self, result: bytes) -> bool:
        result = self._parse_result(result)[-1][-2]
        return ERR_CODES[f'0x{result}'][1]

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
