from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial


class CMD_get_firmware_version(RFIDCommand):
    """ Command get firmware version of CZS6147 controller.
    """

    def __init__(self):
        super().__init__('72')

    def _process_result(self, result: bytes) -> str:
        result = self.bytes_to_hex(result)
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
        r = session.read(self.length + 4)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)

        return r
