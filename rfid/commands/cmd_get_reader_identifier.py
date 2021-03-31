from rfid.commands.factory.rfid_command import RFIDCommand
from serial import Serial


class cmd_get_reader_identifier(RFIDCommand):
    """ Command get reader identifier of CZS6147 controller.

    """

    def __init__(self):
        super().__init__('68')

    def _process_result(self, result: list) -> str:
        if result:
            result = self.bytes_to_hex(result)
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
        s = session.write(self.command)
        r = session.read(self.length + 15)
        print(f"Rx: {self.printable_bytestring(r)}")
        if r:
            r = callback(self, r)

        return r
