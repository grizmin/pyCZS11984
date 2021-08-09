from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial
from time import sleep


class cmd_get_firmware_version(RFIDCommand):
    """ Command get firmware version of CZS6147 controller.
    """
    default_timeout = 0.1
    def __init__(self):
        super().__init__('72')

    def _process_result(self, result: bytes) -> str:
        result = self._parse_result(result)[-1]
        major = result[-3]
        minor = result[-2]
        return f"{major}.{minor}"

    def __call__(self, session: Serial, callback=_process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            callback: callback results processor.
            session: Serial session.
        """
        print(f"Tx: {self.printable_command}")
        s = session.write(self.command)
        session.write(self.command)
        sleep(self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)

        return r
