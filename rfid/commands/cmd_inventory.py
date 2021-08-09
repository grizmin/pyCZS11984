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
    freq_map = {
        0: '865',
        1: '865.5',
        2: '866',
        3: '866.5',
        4: '867',
        5: '867.5',
        6: '868',
        7: '902',
        8: '902.5',
        9: '903',
        10: '903.5',
        11: '904',
        12: '904.5',
        13: '905',
        14: '905.5',
        15: '906',
        16: '906.5',
        17: '907',
        18: '907.5',
        19: '908',
        20: '908.5',
        21: '909',
        22: '909.5',
        23: '910',
        24: '910.5',
        25: '911',
        26: '911.5',
        27: '912',
        28: '912.5',
        29: '913',
        30: '913.5',
        31: '914',
        32: '914.5',
        33: '915',
        34: '915.5',
        35: '916',
        36: '916.5',
        37: '917',
        38: '917.5',
        39: '918',
        40: '918.5',
        41: '919',
        42: '919.5',
        43: '920',
        44: '920.5',
        45: '921',
        46: '921.5',
        47: '922',
        48: '922.5',
        49: '923',
        50: '923.5',
        51: '924',
        52: '924.5',
        53: '925',
        54: '925.5',
        55: '926',
        56: '926.5',
        57: '927',
        58: '927.5',
        59: '928'
    }

    rssi_map = {
        98: '-31',
        97: '-32',
        96: '-33',
        95: '-34',
        94: '-35',
        93: '-36',
        92: '-37',
        91: '-38',
        90: '-39',
        89: '-41',
        88: '-42',
        87: '-43',
        86: '-44',
        85: '-45',
        84: '-46',
        83: '-47',
        82: '-48',
        81: '-49',
        80: '-50',
        79: '-51',
        78: '-52',
        77: '-53',
        76: '-54',
        75: '-55',
        74: '-56',
        73: '-57',
        72: '-58',
        71: '-59',
        70: '-60',
        69: '-61',
        68: '-62',
        67: '-63',
        66: '-64',
        65: '-65',
        64: '-66',
        63: '-67',
        62: '-68',
        61: '-69',
        60: '-70',
        59: '-71',
        58: '-72',
        57: '-73',
        56: '-74',
        55: '-75',
        54: '-76',
        53: '-77',
        52: '-78',
        51: '-79',
        50: '-80',
        49: '-81',
        48: '-82',
        47: '-83',
        46: '-84',
        45: '-85',
        44: '-86',
        43: '-87',
        42: '-88',
        41: '-89',
        40: '-90',
        39: '-91',
        38: '-92',
        37: '-93',
        36: '-94',
        35: '-95',
        34: '-96',
        33: '-97',
        32:  '-98',
        31: '-99'
    }

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
            stats = result[-1]
            # print(result)
            num_tags = int("".join(stats[-5:-1]), 16)
            read_rate = int("".join(stats[-7:-5]), 16)
            antenna_id = int(stats[4], 16)

            def parse_tag_packet(tag_packet: list):
                p = tag_packet

                tag_epc = p[7:-2]
                tag_pc = p[5:7]
                tag_rssi = self.rssi_map[int(p[-2], 16)]

                # The high 6 bits are frequency parameter; the low 2 bits are antenna ID
                tag_freq = self.freq_map[int(f"{int(p[4], 16):08b}"[2:], 2)]
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
