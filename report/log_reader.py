# log_parser.py

class LogParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.commands = {}

    def parse(self, keywords):
        commands = {keyword: {} for keyword in keywords}
        current_command = None

        with open(self.filepath, 'r') as file:
            for line in file:
                if line.startswith('AUTO>'):
                    command_line = line.strip()[5:].strip()
                    for keyword in keywords:
                        if command_line.startswith(keyword + ' '):
                            if command_line not in commands[keyword]:
                                commands[keyword][command_line] = {'command': command_line, 'output': ''}
                            current_command = commands[keyword][command_line]
                            break
                    else:
                        current_command = None
                elif current_command is not None:
                    current_command['output'] += line
        self.commands = commands
        
    def get_commands(self):
        return self.commands
