from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial


class cmd_get_reader_temperature(RFIDCommand):
    """ Command get temperature of CZS6147 controller.

        My test unit doesn't support that one.
        I can't test if works.
    """

    def __init__(self, cmd='7B'):
        super().__init__(cmd)

    def _process_result(self, result: list) -> str:
        result = self.bytes_to_hex(result)
        # if 5th byte == 1 -> temperature is negative.
        reader_temperature = int(result[-2], 16) if int(result[-3], 16) else -int(result[-2], 16)
        return {"temperature": reader_temperature}

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
        if r:
            r = callback(self, r)

        return r
