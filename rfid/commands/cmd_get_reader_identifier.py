from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial
from time import sleep


class cmd_get_reader_identifier(RFIDCommand):
    """ Command get reader identifier of CZS6147 controller.

    """
    default_timeout = 0.1
    cmd = '68'
    def __init__(self):
        super().__init__(self.cmd)

    def _process_result(self, result: list) -> str:
        if result:
            result = self._parse_result(result)[-1]
            reader_id = result[-14:-2]
            return {"reader_id": reader_id}
        return 'Controller returned nothing'


    def __call__(self, session: Serial, callback=_process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            callback: callback results processor.
            session: Serial session.
        """
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.default_timeout+1)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        if r:
            r = callback(self, r)

        return r
