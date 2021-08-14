from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES, RSSI_MAP, FREQ_MAP, DEFAULT_TIMEOUT


class cmd_inventory(RFIDCommand):
    """ Command inventory of CZS6147 controller.

        host packet
        [Head | Len | Address | Cmd | Repeat interval | Checksum ]
        [ A0  | 04  |         |  80 |                 |          ]

        repeat interval - Repeat time of inventory round.
        When Repeat = 255, The inventory duration is minimized.
        For example, if the RF field only has one or two tags,
        the inventory duration could be only 30-50 mS,
        this function provides a possibility for fast antenna
        switch applications on multi-ant devices.
        Documentation does not provide definition of what this humber representation in time units is.
        I think it's deciseconds (centisecond) and this is how I am implementing it.


        response packets
        [ Head | Len | Address | Cmd | AntID | TagCount | ReadRate | TotalRead | Check ]
        [ 0xA0 |0x0C | 1Byte   |0x80 | 1Byte | 2 Bytes  | 2Bytes   | 4Bytes    | 1Byte ]


    """
    cmd_inventory = '80'

    def __init__(self, scan_duration: int):
        self.scan_duration = scan_duration


    @property
    def repeat_interval(self) -> int:
        """
        Returns: repeat interval parameter.
        """
        return self._repeat_interval

    @repeat_interval.setter
    def repeat_interval(self, repeat_interval: int) -> None:
        assert 1 <= repeat_interval <= 255, "Scan duration. Accepted values are in range 0-255."
        self._repeat_interval = repeat_interval
        super().__init__(self.cmd_rt_inventory, param_data=[self.repeat_interval])


    def _process_result(self, result: bytes) -> bool:
        """
        response packet example:
        [ Head | Len | Address | Cmd | AntID | TagCount | ReadRate | TotalRead | Check ]
        [ 0xA0 |0x0C | 1Byte   |0x80 | 1Byte | 2 Bytes  | 2Bytes   | 4Bytes    | 1Byte ]
        """
        if result:
            result = self._parse_result(result)
            stats = result[-1]
            # print(result)

            # TotalRead
            num_tags = int("".join(stats[-5:-1]), 16)
            # ReadRate
            read_rate = int("".join(stats[-7:-5]), 16)
            # AntId
            antenna_id = int(stats[4], 16)

            def parse_tag_packet(tag_packet: list):
                p = tag_packet
                # EPC
                tag_epc = p[7:-2]
                # PC
                tag_pc = p[5:7]
                # RSSI
                tag_rssi = self.RSSI_MAP[int(p[-2], 16)]

                # The high 6 bits are frequency parameter; the low 2 bits are antenna ID
                tag_freq = self.FREQ_MAP[int(f"{int(p[4], 16):08b}"[2:], 2)]
                tag_antenna_id = int(f"{int(p[4], 16):08b}"[:2], 2)

                data_object = {
                    "tag_epc": tag_epc,
                    "tag_pc": tag_pc,
                    "tag_rssi": tag_rssi,
                    "tag_freq": tag_freq,
                    "tag_antenna_id": tag_antenna_id
                }
                return data_object

            tags_data = {
                "num_tags": num_tags,
                "read_rate": read_rate,
                "antenna_id": antenna_id,
                "tags": []
            }

            for tag in result[:-1]:
                tags_data["tags"].append(parse_tag_packet(tag))

            return {'result': tags_data}
        return 'Command returned nothing.'

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result, interval=None) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
            interval: sets the time interval in deciseconds (centisecond) the controller will scan for tags before yielding results.
        """
        if interval:
            self.repeat_interval = interval
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.repeat_interval/10+DEFAULT_TIMEOUT)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        # print(r)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
