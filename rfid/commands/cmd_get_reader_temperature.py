from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial
from time import sleep

class cmd_get_reader_temperature(RFIDCommand):
    """ Command get temperature of CZS6147 controller.

        My test unit doesn't support that one.
        I can't test if works.
    """
    default_timeout = 0.1
    def __init__(self, cmd='7B'):
        super().__init__(cmd)

    def _process_result(self, result: list) -> str:
        result = self._parse_result(result)
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
        session.write(self.command)
        sleep(self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        if r:
            r = callback(self, r)

        return r
