class CommandHandler:
    def __init__(self, command_name):
        self.command_name = command_name

    def handle_output(self, output):
        # Implement the logic to handle the output of the command
        pass


class ShowLineCommandHandler(CommandHandler):
    def __init__(self):
        super().__init__('showline')

    def handle_output(self, output):
        # Implement the logic to handle the output of the 'showline' command
        pass


# Add more command handlers for other commands as needed


command_handlers = {}


def register_command_handler(handler_class):
    command_handlers[handler_class().command_name] = handler_class


def get_command_handler(command_name):
    handler_class = command_handlers.get(command_name)
    if handler_class:
        return handler_class()
    else:
        return None