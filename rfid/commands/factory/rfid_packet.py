from typing import List


class RFIDPacketException(Exception):
    pass


class RFIDPacket:
    """
    Definition of data packets
    [ Head | Len | Address | Cmd | Data[0…N] | Check ]
        |     |       |       |       |         |
        |     |       |       |       |         |> (1 Byte) Checksum. Check all the bytes except itself.
        |     |       |       |       |> (n Bytes) Command parameters
        |     |       |       |> (1 Byte) Command byte (list of commands)
        |     |       |> (1 Byte) Reader’s address. The common addresses are 0~ 254(0xFE)，
        |     |          255(0xFF) is the public address.
        |     |          The reader accepts the address of itself and the public address.
        |     |> (1 Byte) Length of the packet bytes. Starts from the third byte.
        |> (1 Byte) Head of the packet. (Always 0xA0)

    Definition of response data packets
    [ Head | Len | Address | Data[0…N] | Check ]
        |     |       |       |            |
        |     |       |       |            |> (1 Byte) Checksum. Check all the bytes except itself.
        |     |       |       |> (n Bytes) Data from the reader
        |     |       |> (1 Byte) Reader’s address.
        |     |> (1 Byte) Length of the packet bytes. Starts from the third byte.
        |> (1 Byte) Head of the packet. (Always 0xA0)
    """

    # Definition of commands and packets
    PACKET_HEAD = 0xA0

    # Component index in the array of bytes
    INDEX_HEAD = 0
    INDEX_LENGTH = 1
    INDEX_ADDRESS = 2
    INDEX_CMD = 3
    INDEX_DATA_START = 4

    BYTEORDER = 'big'

    def __init__(self, address, cmd, data=[], head=0x00, length=0x00, check=0x00, byteorder='big'):
        """
        Represents common IND903/CSZ6174 controller packet.
        Args:
            address: (1 Byte) Reader’s address. The common addresses are 0~ 254(0xFE).
            cmd: (1 Byte) Command byte (list of commands).
            data: (n Bytes) Command parameters.
            head: (1 Byte) Head of the packet. (Always 0xA0).
            length: (1 Byte) Length of the packet bytes. Starts from the third byte.
            check: (1 Byte) Checksum. Check all the bytes except itself.
            byteorder: self explanatory.
        """
        self.BYTEORDER = byteorder
        #TODO convert to properties
        self._head = head if isinstance(head, bytes) else \
                    head.to_bytes(1, byteorder=byteorder, signed=False)
        self._address = address if isinstance(address, bytes) else \
                       address.to_bytes(1, byteorder=byteorder, signed=False)
        self._cmd = cmd if isinstance(cmd, bytes) else \
                   cmd.to_bytes(1, byteorder=byteorder, signed=False)
        self._data = data if isinstance(data, bytes) else \
                    b''.join(list(map(self.int_to_bytes, data)))
        self._length = length if isinstance(length, bytes) else \
                      self.calculate_packet_length(self._data)\
                      .to_bytes(1, byteorder=byteorder, signed=False)
        subpacket = b''.join([self._head + self._length + self._address + self._cmd + self._data])
        self._check = check if isinstance(check, bytes) else self.checksum8bit(subpacket)
        self.packet = bytearray(subpacket + self._check)

    def __repr__(self):
        repr = self.to_string()
        return repr

    @staticmethod
    def parse_packet(packetData, byteorder='big'):
        """
        Static method to parse and extract the packet information into the structure
        :param packetData: hexadecimal bytes corresponding to the packet
        """
        try:
            packet = bytearray(packetData)
            _head = packet[RFIDPacket.INDEX_HEAD].to_bytes(1, byteorder=byteorder, signed=False)
            _length = packet[RFIDPacket.INDEX_LENGTH].to_bytes(1, byteorder=byteorder, signed=False)
            _address = packet[RFIDPacket.INDEX_ADDRESS].to_bytes(1, byteorder=byteorder, signed=False)
            _cmd = packet[RFIDPacket.INDEX_CMD].to_bytes(1, byteorder=byteorder, signed=False)
            _data = bytearray(packet[RFIDPacket.INDEX_DATA_START:len(packet)-1])
            _check = packet[len(packet)-1].to_bytes(1, byteorder=byteorder, signed=False)
            return RFIDPacket(_address, _cmd, head=_head, length=_length, data=_data, check=_check)
        except Exception as ex:
            raise RFIDPacketException('Error parsing packet ' + packetData)

    @property
    def cmd(self):
        return hex(int.from_bytes(self._cmd, 'big'))

    @property
    def address(self):
        return hex(int.from_bytes(self._address, 'big'))

    @property
    def data(self):
        return hex(int.from_bytes(self._data, 'big'))

    def to_string(self):
        """
        :return: The complete packet as a list of bytes in a string
        """
        return " ".join([f"{v:02x}".upper() for v in self.packet])

    def to_list(self):
        """
        :return: The complete packet as a list of bytes in a string
        """
        return [f"{v:02x}".upper() for v in self.packet]

    @staticmethod
    def calculate_packet_length(data: List[int] = []):
        """
        Length starts from 3rd byte.
        what counts: address, command, data, checksum
            - address is always 1 byte
            - command is always 1 byte
            - checksum is always 1 byte
        we just need the length of the data (parameters)

        length = 3 + len(data)

        """
        length = 3 + sum([(i.bit_length()+7)//8 for i in data])
        return length

    @classmethod
    def checksum8bit(cls, data: bytearray) -> int:
        """

        Args:
            data: data parameter

        Returns:
               checksum as bytes
        """
        return (((sum(data) ^ 0xFF) + 1) & 0xFF).to_bytes(1, byteorder=cls.BYTEORDER)

    @staticmethod
    def generate_packet(data: bytes) -> RFIDPacket:
        """

        Args:
            data: data parameter

        Returns:

        """
        return RFIDPacket.parse_packet(bytearray(data + RFIDPacket.checksum8bit(data)))

    @staticmethod
    def int_to_bytes(x: int) -> bytes:
        """
        Args:
            x: integer to convert in bytes

        Returns: bytes

        """
        length = (x.bit_length() + 7) // 8 or 1
        return x.to_bytes(length, 'big')
