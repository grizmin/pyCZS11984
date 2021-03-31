import serial
from typing import List
from serial.tools import list_ports


def props(cls: object) -> List[str]:
    return [i for i in cls.__dict__.keys() if i[:1] != '_']


def list_devices() -> None:
    for device in list_ports.comports():
        print(f"*** Device: {list_ports.comports().index(device)} ***")
        for p in [prop for prop in props(device) if prop != 'device']:
            print(f"{p}: {getattr(device, p)}")


def get_device_by_serial(serial_number: str) -> str:
    return next(list_ports.grep(serial_number)).device


class RFIDSession():
    def __init__(self, device: str):
        self.device = device.upper()

    def session(self, baudrate: int = 115200, timeout: int = 1):

        ser = serial.Serial(self.device, baudrate, timeout=timeout)
        print(f"{self.device} is {'open' if ser.is_open else 'closed'}.")
        for setting in ser.get_settings():
            print(f"{setting:20}:{ser.get_settings()[setting]}")
        return ser


