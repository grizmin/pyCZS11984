from typing import List
from rfid.commands.factory.command_type import RFIDCommandType
from .rfid_packet import RFIDPacket

class RFIDCommand(RFIDCommandType):
    HEADER = 0xA0

    def __init__(self, cmd: str, param_data: List = [], addr: int = 0x01, length: int = 0x03):
        self.cmd = cmd
        self.addr = addr
        self.length = length
        self.param_data = param_data
        self.packet = self.__build_command()

    @property
    def command(self) -> bytes:
        return self.packet.packet

    def __repr__(self):
        return str(self.printable_command)

    @staticmethod
    def flatten(lst):
        return [item for sublist in lst for item in sublist]

    @property
    def printable_command(self):
        return self.printable_bytestring(self.command)

    @staticmethod
    def printable_bytestring(val):
        return " ".join([f"{v:02x}".upper() for v in val])

    @staticmethod
    def bytes_to_hex(val):
        return [f"{v:02x}".upper() for v in val]

    @staticmethod
    def checksum8bit(data: bytearray) -> int:
        check = ((sum(data) ^ 0xFF) + 1) & 0xFF
        return check.to_bytes(1, 'big')

    @staticmethod
    def string_to_bytearray(string: str) -> bytes:
        return bytes.fromhex(string)

    @staticmethod
    def int_to_bytes(x: int) -> bytes:
        length = (x.bit_length() + 7) // 8 or 1
        return x.to_bytes(length, 'big')

    @staticmethod
    def int_from_bytes(xbytes: bytes) -> int:
        return int.from_bytes(xbytes, 'big')

    @staticmethod
    def _parse_result(data: list) -> list:
        data = RFIDCommand.bytes_to_hex(data)
        command_indexes = []
        commands = []
        for idx in range(len(data)):
            if data[idx] == "A0":
                # print(f"Command start found at {idx}")
                command_indexes.append(idx)

        for idx in range(len(command_indexes)):
            start = command_indexes[idx]
            end = command_indexes[idx + 1] if len(command_indexes) > idx + 1 else None
            commands.append(data[start:end])

        for command in commands:
            received_checksum = command[-1]
            calculated_checksum = RFIDCommand.bytes_to_hex(RFIDPacket.checksum8bit(RFIDCommand.string_to_bytearray("".join(command[:-1]))))
            if received_checksum != received_checksum:
                print(f"Checksum mismatch. received_checksum: {received_checksum}, calculated_checksum: {calculated_checksum}, packet: {command}")

        return commands

    def _process_result(self, result: list) -> str:
        if result:
            commands = RFIDCommand._parse_result(result)
            return commands[-1]
        else:
            return ""

    def __build_command_v1(self) -> bytearray:
        if self.param_data:
            # Big integers might be several bytes.
            bytes_data = map(self.int_to_bytes, self.param_data)
        byte_command = bytearray([self.HEADER, RFIDCommand.calculate_packet_length(self.param_data), self.addr, int(self.cmd, 16)]) + \
                        b''.join(list(map(self.int_to_bytes, self.param_data)))
        # ### debug - remove
        # print(byte_command)

        byte_command += self.checksum8bit(byte_command)
        return byte_command

    def __build_command(self, data=[]) -> RFIDPacket:
        subcommand = [
            self.addr,
            int(self.cmd, 16)
        ]
        if data:
            return RFIDPacket(*subcommand, data=data)
        return RFIDPacket(*subcommand, data=self.param_data)


    @staticmethod
    def calculate_packet_length(data: List[int] = []):
        # Length starts from 3rd byte.
        # what we have after 3rd byte is: command, data, checksum
        # command is always 1 byte
        # checksum is always 1 byte
        # we just need the length of the data (parameters)
        # length = 3 + data
        length = 3 + sum([(i.bit_length()+7)//8 for i in data])
        return length
