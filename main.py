from rfid.communication import RFIDSession, list_devices, get_device_by_serial
from rfid.commands.factory.commands import command

def main():
    print("List devices")
    list_devices()

    ## serial to search for
    serial_number = '66D931950028E8119298E24AA9A0087C'
    device = get_device_by_serial(serial_number)

    with RFIDSession(device).session(timeout=20) as s:

        cmd_reset = command('cmd_reset')
        cmd_version = command('cmd_get_firmware_version')
        cmd_get_output_power = command('cmd_get_output_power')
        cmd_get_frequency_region = command('cmd_get_frequency_region')
        cmd_get_reader_identifier = command('cmd_get_reader_identifier')
        cmd_get_reader_temperature = command('cmd_get_reader_temperature')
        cmd_get_rf_link_profile = command('cmd_get_rf_link_profile')
        cmd_get_rf_port_return_loss = command('cmd_get_rf_port_return_loss')
        cmd_get_work_antenna = command('cmd_get_work_antenna')
        inventory = command('cmd_inventory', 2)
        cmd_read_gpio_value = command('cmd_read_gpio_value')
        # cmd_set_beeper_mode = command('cmd_set_beeper_mode', 1)
        # cmd_set_uart_baudrate = command('cmd_set_uart_baudrate', 115200)


        cmd_version(s)
        # cmd_write_gpio = command('cmd_write_gpio_value', [3, 0])


if __name__ == '__main__':
    main()
