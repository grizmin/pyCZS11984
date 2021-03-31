from rfid.communication import RFIDSession, list_devices, get_device_by_serial
from rfid.commands.factory.commands import command

def main():
    print("List devices")
    list_devices()

    ## serial to search for
    serial_number = '66D931950028E8119298E24AA9A0087C'
    device = get_device_by_serial(serial_number)

    with RFIDSession(device).session(timeout=0.1) as s:
        ## cmd_reset
        cmd_reset = command('cmd_reset')
        # cmd_write_gpio = command('cmd_write_gpio_value', [3, 0])


if __name__ == '__main__':
    main()
