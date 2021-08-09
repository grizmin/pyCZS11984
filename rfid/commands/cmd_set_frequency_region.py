from rfid.commands.factory.rfid_command import RFIDCommand
from typing import Callable, List
from serial import Serial
from time import sleep
from . constants import ERR_CODES


class cmd_set_frequency_region(RFIDCommand):
    """ Command set frequency of CZS6147 controller.
        The baudrate will be written to persistent memory.

        Regions:
        0x01 FCC
        0x02 ETSI
        0x03 CHN

        Freqs:
        0(0x00) 865.00 MHz
        1(0x01) 865.50 MHz
        2(0x02) 866.00 MHz
        3(0x03) 866.50 MHz
        4(0x04) 867.00 MHz
        5(0x05) 867.50 MHz
        6(0x06) 868.00 MHz
        7(0x07) 902.00 MHz
        8(0x08) 902.50 MHz
        9(0x09) 903.00 MHz
        10(0x0A) 903.50 MHz
        11(0x0B) 904.00 MHz
        12(0x0C) 904.50 MHz
        13(0x0D) 905.00 MHz
        14(0x0E) 905.50 MHz
        15(0x0F) 906.00 MHz
        16(0x10) 906.50 MHz
        17(0x11) 907.00 MHz
        18(0x12) 907.50 MHz
        19(0x13) 908.00 MHz
        20(0x14) 908.50 MHz
        21(0x15) 909.00 MHz
        22(0x16) 909.50 MHz
        23(0x17) 910.00 MHz
        24(0x18) 910.50 MHz
        25(0x19) 911.00 MHz
        26(0x1A) 911.50 MHz
        27(0x1B) 912.00 MHz
        28(0x1C) 912.50 MHz
        29(0x1D) 913.00 MHz
        30(0x1E) 913.50 MHz
        31(0x1F) 914.00 MHz
        32(0x20) 914.50 MHz
        33(0x21) 915.00 MHz
        34(0x22) 915.50 MHz
        35(0x23) 916.00 MHz
        36(0x24) 916.50 MHz
        37(0x25) 917.00 MHz
        38(0x26) 917.50 MHz
        39(0x27) 918.00 MHz
        40(0x28) 918.50 MHz
        41(0x29) 919.00 MHz
        42(0x2A) 919.50 MHz
        43(0x2B) 920.00 MHz
        44(0x2C) 920.50 MHz
        45(0x2D) 921.00 MHz
        46(0x2E) 921.50 MHz
        47(0x2F) 922.00 MHz
        48(0x30) 922.50 MHz
        49(0x31) 923.00 MHz
        50(0x32) 923.50 MHz
        51(0x33) 924.00 MHz
        52(0x34) 924.50 MHz
        53(0x35) 925.00 MHz
        54(0x36) 925.50 MHz
        55(0x37) 926.00 MHz
        56(0x38) 926.50 MHz
        57(0x39) 927.00 MHz
        58(0x3A) 927.50 MHz
        59(0x3B) 928.00 MHz
    """

    default_timeout = 0.1

    def __init__(self, frequency_params: List[int]):
        self.freq_params = frequency_params
        super().__init__('78', param_data=self.freq_params)

    @property
    def freq_params(self) -> List[int]:
        """
        Returns: frequency parameter list.
        """
        return self._freq_params

    @freq_params.setter
    def freq_params(self, freq_params: List[int]) -> None:
        assert 1 <= freq_params[0] <= 3, "Spectrum region must be 0x01 FCC, 0x02 ETSI, 0x03 CHN"
        assert 0 <= freq_params[1] <= 59, "Start frequency must be in range 0-59"
        assert 0 <= freq_params[2] <= 59, "End frequency must be in range 0-59"
        self._freq_params = freq_params

    def _process_result(self, result: bytes) -> bool:
        r = self._parse_result(result)[-1][-2]
        return ERR_CODES[f'0x{r}'][1]

    def __call__(self, session: Serial,
                 callback: Callable[[bytes], bool] = _process_result) -> list[str]:
        """
        sends the command to the specified serial session.
        Args:
            session: Serial session
        """
        print(f"Tx: {self.printable_command}")
        session.write(self.command)
        sleep(self.default_timeout)
        in_waiting = session.in_waiting
        r = session.read(in_waiting)
        print(f"Rx: {self.printable_bytestring(r)}")
        r = callback(self, r)
        return r
