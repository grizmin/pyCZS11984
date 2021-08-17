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
        rt_inventory = command('cmd_rt_inventory', 2)
        inventory = command('cmd_inventory', 5)
        cmd_read = command("cmd_read", 1, 0, 7)
        # cmd_read(s, mem_bank=1, word_address=0, word_count=7)
        cmd_read_gpio_value = command('cmd_read_gpio_value')
        cmd_set_beeper_mode = command('cmd_set_beeper_mode', 1)
        cmd_set_uart_baudrate = command('cmd_set_uart_baudrate', 115200)


        cmd_version(s)
        # print all tags
        # rt_inventory command supports interval parameter, which supersedes instance parameter.
        # E.G. inventory(s, interval=10)
        print("\n".join([f"{id}) tagid: {tagid}" for id, tagid in enumerate(["".join(tag["tag_epc"]) for tag in rt_inventory(s, interval=10)["result"]["tags"]])]))

        # cmd_write_gpio = command('cmd_write_gpio_value', [3, 0])


if __name__ == '__main__':
    main()
