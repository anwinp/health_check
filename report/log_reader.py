# log_parser.py

class LogParser:
    def __init__(self, filepath, command_key_to_fetch_pattern):
        self.filepath = filepath
        self.commands = {}
        self.command_key_to_fetch_pattern = command_key_to_fetch_pattern

    def expand_fetch_patterns(self, patterns):
        """Expand fetch patterns to recognize both parameterized and non-parameterized commands."""
        expanded_patterns = {}
        for command, pattern_list in patterns.items():
            expanded = set()
            for pattern in pattern_list:
                expanded.add(pattern)
                if pattern.endswith('*'):
                    base = pattern[:-1]
                    expanded.add(base)  # Also recognize the base command without parameters
            expanded_patterns[command] = expanded
        return expanded_patterns

    def parse(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()

        active_commands = []
        for line in lines:
            line = line.strip()
            if line.startswith('AUTO>'):
                command_line = line[5:].strip()
                active_commands = []  # Reset active commands for each new command line
                for base_command, pattern_set in self.command_key_to_fetch_pattern.items():
                    if any(command_line == pattern or command_line.startswith(pattern[:-1]) for pattern in pattern_set):
                        if base_command not in self.commands:
                            self.commands[base_command] = {}
                        if command_line not in self.commands[base_command]:
                            self.commands[base_command][command_line] = {'command': command_line, 'output': ''}
                        active_commands.append(base_command)  # Track all commands that match the line
            elif active_commands:
                # Append the line to the output of all active base commands
                for base_command in active_commands:
                    if command_line in self.commands[base_command]:
                        self.commands[base_command][command_line]['output'] += line + '\n'


    
    def get_commands(self):
        return self.commands

    def parse_new(self, keywords):
        # Reset commands dictionary
        self.commands = {}

        with open(self.filepath, 'r') as file:
            current_command_key = None
            for line in file.readlines():
                line = line.strip()
                if line.startswith('AUTO>'):
                    command_line = line[len('AUTO>'):].strip()
                    for keyword in keywords:
                        # Check for wildcard in the keyword
                        if '*' in keyword:
                            # Remove wildcard and check if command_line starts with the base keyword
                            base_keyword = keyword.replace(' *', '')
                            if command_line.startswith(base_keyword) and len(command_line.split()) > len(base_keyword.split()):
                                # Command matches the keyword with an additional parameter
                                self.commands[command_line] = {'command': command_line, 'output': ''}
                                current_command_key = command_line
                                break
                        elif command_line == keyword:
                            # Exact match without additional parameters
                            self.commands[command_line] = {'command': command_line, 'output': ''}
                            current_command_key = command_line
                            break
                    else:
                        # Reset current command if no keywords match
                        current_command_key = None
                elif current_command_key:
                    # Append to the output of the current command
                    self.commands[current_command_key]['output'] += line + '\n'
    