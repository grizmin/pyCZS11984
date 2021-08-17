from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES, RSSI_MAP, FREQ_MAP, DEFAULT_TIMEOUT


class cmd_read(RFIDCommand):
    """ Command inventory of CZS6147 controller.

        host packet
        [Head | Len | Address | Cmd | MemBank | WordAdd | WordCnt  | Checksum ]
        [ A0  | 06  |  1 Byte |  81 | 1 Byte  | 1 Byte  | 1 Byte   |          ]

        Mem Bank:
            0x00 - RESERVED
            0x01 - EPC
            0x02 - TID
            0x03 - USER

        WordAdd (Read start address): Please see the tag’s spec for more information.
        WordCnt (Read data length): Data length in WORD(16bits) unit. Please see the tag’s spec for more information.

        response packets
        [ Head | Len | Address | Cmd | TagCount | DataLen | Data    | ReadLen | AntID | ReadCount | Check  ]
        [ 0xA0 |0x0C | 1Byte   |0x80 | 2 Bytes  | 1 Byte  | n Bytes | 1 Byte  | 1 Byte| 1 Byte    | 1 Byte ]


    """
    cmd_read = '81'

    def __init__(self, mem_bank: int, word_address: int, word_count: int):
        self.mem_bank = mem_bank
        self.word_address = word_address
        self.word_count = word_count
        super().__init__(self.cmd_read, param_data=[self.mem_bank, self.word_address, self.word_count])

    @property
    def mem_bank(self) -> int:
        """
        Returns: repeat interval parameter.
        """
        return self._mem_bank

    @mem_bank.setter
    def mem_bank(self, mem_bank: int) -> None:
        assert 0 <= mem_bank <= 3, "Scan duration. Accepted values are in range 0-255."
        self._mem_bank = mem_bank

    def _process_result(self, result: bytes) -> bool:
        """
        response packets
        [ Head | Len | Address | Cmd | TagCount | DataLen | Data    | ReadLen | AntID  | ReadCount | Check  ]
        [ 0xA0 |0x0C | 1Byte   |0x80 | 2Byte    | 1 Byte  | n Bytes | 1 Bytes | 1 Byte | 1 Byte    | 1 Byte ]

        response packet example:
        [ Head | Len | Address | Cmd | TagCount | DataLen | Data    | ReadLen | AntID  | ReadCount | Check  ]
        ['A0',
                '27',
                        '01',
                                '81',
                                     '00', '01',
                                                    '1E',
                                                           '30', '00', 'E2', '00', '00', '19', '11', '05', '01', '07', '11', '10', '51', '25', 'C5', 'A9', '30', '00', 'E2', '00', '00', '19', '11', '05', '01', '07', '11', '10', '51', '25',
                                                                     '0E',
                                                                               '14',
                                                                                           '01',
                                                                                                      '47']
        """
        if result:
            result = self._parse_result(result)

            # handle error
            if int(result[-1][1], 16) == 4:
                print(ERR_CODES[f'0x{result[-1][-2]}'][0], ':', ERR_CODES[f'0x{result[-1][-2]}'][1])
                return {'error': ERR_CODES[f'0x{result[-1][-2]}']}

            print(result)
            data = result[-1]

            reader_address = int(data[2], 16)
            cmd = int(data[3], 16)
            # TagCount
            tag_count = int("".join(data[4:6]), 16)
            # DataLen
            data_len = int(data[6], 16)
            # ReadCount
            read_count = int("".join(data[-2]), 16)
            # The high 6 bits are frequency parameter; the low 2 bits are antenna ID
            freq = FREQ_MAP[int(f"{int(data[-3], 16):08b}"[2:], 2)]
            antenna_id = int(f"{int(data[-3], 16):08b}"[:2], 2)
            # ReadLen
            read_len = int(data[-4], 16)
            # data
            data = data[7:data_len+7+1]
            # PC
            pc = data[:2]
            # EPC
            epc = data[2:14]
            # crc
            crc = data[14:16]
            # read_data
            read_data = data[16:]


            tags_data = {
                "reader_address": reader_address,
                "cmd": cmd,
                "tag_count": tag_count,
                "data_len": data_len,
                "read_count": read_count,
                "antenna_id": antenna_id,
                "freq": freq,
                "read_len": read_len,
                "data": data,
                "decoded_data": {
                    "pc": pc,
                    "epc": epc,
                    "crc": crc,
                    "read_data": read_data
                }
            }

            return {'result': tags_data}
        return 'Command returned nothing.'

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result, mem_bank=None, word_address=None, word_count=None) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
            interval: sets the time interval in deciseconds (centisecond) the controller will scan for tags before yielding results.
        """
        self.mem_bank = mem_bank if mem_bank else self.mem_bank
        self.word_address = word_address if word_address else self.word_address
        self.word_count = word_count if word_count else self.word_count
        super().__init__(self.cmd_read, param_data=[self.mem_bank, self.word_address, self.word_count])
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(DEFAULT_TIMEOUT+0.5)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        # print(r)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
