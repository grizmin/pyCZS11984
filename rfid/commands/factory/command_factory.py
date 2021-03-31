from .command_type import RFIDCommandType

class CommandFactory:

    def __init__(self):
        self._creators = {}

    @property
    def commands(self):
        """
        Returns: list of registered commands
        """
        return [key for key in self._creators]

    def register_command(self, command, creator):
        """
        Args:
            command: command name
            creator: creator callable
        """
        self._creators[command] = creator

    def __call__(self, command, *args, **kwargs) -> RFIDCommandType:
        """
        Args:
            command: command name
            *args: args to be passed to command creator
            **kwargs: kwargs to be passed to command creator

        Returns:
        """
        creator = self._creators.get(command)
        if not creator:
            raise ValueError(format)
        return creator(*args, **kwargs)
