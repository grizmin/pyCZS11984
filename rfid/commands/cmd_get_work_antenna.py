from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial


class CMD_get_work_antenna(RFIDCommand):
    """ Command get working antenna of CZS6147 controller.
    """

    def __init__(self):
        super().__init__('75')

    def _process_result(self, result: list) -> str:
        result = self.bytes_to_hex(result)
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
        s = session.write(self.command)
        r = session.read(self.length + 3)
        print(f"Rx: {self.printable_bytestring(r)}")
        if r:
            r = callback(self, r)

        return r
