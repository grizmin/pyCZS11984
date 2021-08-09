from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_inventory(RFIDCommand):
    """ Command rf link profile of CZS6147 controller.
    Repeat time of inventory round.
        When Repeat = 255, The inventory duration is minimized.
        For example, if the RF field only has one or two tags,
        the inventory duration could be only 30-50 mS,
        this function provides a possibility for fast antenna
        switch applications on multi-ant devices.

        Documentation does not provide definition of what this humber representation in time units is.
        I think it's deciseconds (centisecond) and this is how I am implementing it.
    """
    cmd_rt_inventory = '89'
    default_timeout = 0.1

    def __init__(self, scan_duration: int):
        self.scan_duration = scan_duration


    @property
    def scan_duration(self) -> List[int]:
        """
        Returns: frequency parameter list.
        """
        return self._scan_duration

    @scan_duration.setter
    def scan_duration(self, scan_duration: int) -> None:
        assert 1 <= scan_duration <= 255, "Scan duration. Accepted values are in range 0-255."
        self._scan_duration = scan_duration
        super().__init__(self.cmd_rt_inventory, param_data=[self.scan_duration])


    def _process_result(self, result: bytes) -> bool:
        if result:
            result = self._parse_result(result)
            profile = result
            return {'result': profile}
        return 'Command returned nothing.'

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result, interval=None) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        if interval:
            self.scan_duration = interval
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.scan_duration/10+self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        # print(r)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
