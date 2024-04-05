


class ParserFactory:
    def __init__(self):
        self.parsers = {}

    def register_parser(self, command_keyword, parser):
        self.parsers[command_keyword] = parser

    def get_parser(self, command_keyword):
        parser = self.parsers.get(command_keyword)
        if not parser:
            raise ValueError(f"No parser registered for command: {command_keyword}")
        return parser()