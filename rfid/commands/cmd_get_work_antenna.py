from rfid.commands.factory.rfid_command import RFIDCommand
from time import sleep
from serial import Serial


class cmd_get_work_antenna(RFIDCommand):
    """ Command get working antenna of CZS6147 controller.
    """
    default_timeout = 0.5

    def __init__(self):
        super().__init__('75')

    def _process_result(self, result: list) -> str:
        result = self._parse_result(result)[-1]
        antenna = result[-2]
        return f"{antenna}"

    def __call__(self, session: Serial, callback=_process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            callback: callback results processor.
            session: Serial session.
        """
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        if r:
            r = callback(self, r)

        return r
