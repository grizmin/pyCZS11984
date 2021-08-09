# pyCZS11984

## early alpha

commands implemented:


        command = CommandFactory()

        command.register_command('cmd_set_uart_baudrate', cmd_set_uart_baudrate.cmd_set_uart_baudrate)
        command.register_command('cmd_get_firmware_version', cmd_get_firmware_version.cmd_get_firmware_version)
        command.register_command('cmd_get_firmware_version', cmd_get_firmware_version.cmd_get_firmware_version)
        command.register_command('cmd_set_reader_address', cmd_set_reader_address.cmd_set_reader_address)
        command.register_command('cmd_set_work_antenna', cmd_set_work_antenna.cmd_set_work_antenna)
        command.register_command('cmd_get_work_antenna', cmd_get_work_antenna.cmd_get_work_antenna)
        command.register_command('cmd_set_output_power', cmd_set_output_power.cmd_set_output_power)
        command.register_command('cmd_get_output_power', cmd_get_output_power.cmd_get_output_power)
        command.register_command('cmd_set_frequency_region', cmd_set_frequency_region.cmd_set_frequency_region)
        command.register_command('cmd_set_frequency_user_defined', cmd_set_frequency_user_defined.cmd_set_frequency_user_defined)
        command.register_command('cmd_get_frequency_region', cmd_get_frequency_region.cmd_get_frequency_region)
        command.register_command('cmd_set_beeper_mode', cmd_set_beeper_mode.cmd_set_beeper_mode)
        command.register_command('cmd_get_reader_temperature', cmd_get_reader_temperature.cmd_get_reader_temperature)
        command.register_command('cmd_read_gpio_value', cmd_read_gpio_value.cmd_read_gpio_value)
        command.register_command('cmd_write_gpio_value', cmd_write_gpio_value.cmd_write_gpio_value)
        command.register_command('cmd_set_temporary_output_power', cmd_set_temporary_output_power.cmd_set_temporary_output_power)
        command.register_command('cmd_get_reader_identifier', cmd_get_reader_identifier.cmd_get_reader_identifier)
        command.register_command('cmd_get_rf_link_profile', cmd_get_rf_link_profile.cmd_get_rf_link_profile)
        command.register_command('cmd_get_rf_port_return_loss', cmd_get_rf_port_return_loss.cmd_get_rf_port_return_loss)
        command.register_command('cmd_inventory', cmd_inventory.cmd_inventory)
        command.register_command('cmd_reset', cmd_reset.cmd_reset)
