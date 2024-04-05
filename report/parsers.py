
import re
from collections import defaultdict

class CommandParserBase:
    def parse(self, blocks):
        raise NotImplementedError("Each parser must implement the parse method.")
    
    def merge_parsed_data(self, parsed_data):
        merged_data = []
        for key in parsed_data:
            merged_data.extend(parsed_data[key])
        return merged_data
    
class ShowlineParser(CommandParserBase):
    def parse(self, blocks, merge=True):
        """
        Parse log data from 'showline' commands into a dictionary format.

        :param log_data: Dictionary containing command outputs
        :return: Dictionary with parsed data ready for report generation
        """
        pattern = re.compile(
            r'shelf = (\d+),\s+slot = (\w+),\s+line type = (\w+).*?line\n(.*?)(?=\nshelf = |\Z)',
            re.MULTILINE | re.DOTALL
        )
        port_pattern = re.compile(r'(\d+-\d+|\d+)\s+(.+)')
        parsed_data = {}

        for command_key, command_data in blocks.items():
            if command_key.startswith('showline'):
                matches = pattern.findall(command_data['output'])
                parsed_data[command_key] = []

                for shelf, slot, line_type, port_statuses in matches:
                    for line in port_statuses.strip().split('\n'):
                        line = line.strip()
                        # Skip dashed lines
                        if '---' in line or not line:
                            continue

                        # Match the port range and status
                        port_match = port_pattern.match(line)
                        if port_match:
                            port_range, status = port_match.groups()
                            parsed_data[command_key].append({
                                'Shelf': shelf,
                                'Slot': slot,
                                'Line Type': line_type,
                                'Port Range': port_range,
                                'Status': status.strip()
                            })

        if merge:
            return self.merge_parsed_data(parsed_data)
        else:
          return parsed_data


    
    
class SlotsParser(CommandParserBase):
    """_summary_
    """
    def __init__(self):
            self.pattern = re.compile(
            r"Type\s+:\s*(?P<Type>[\w\s-]+?),\s*.*?"
            r"Card Version\s+:\s*(?P<Card_Version>[\w-]+)\s.*?"
            r"Software Version:\s*(?P<Software_Version>[\w\.]+)\s.*?"
            r"Shelf\s+:\s*(?P<Shelf>\d+)\s.*?"
            r"Slot\s+:\s*(?P<Slot>\w+)\s.*?"
            r"Uptime\s+:\s*(?P<Uptime>\d+\s+days?,\s+\d+\s+hours?,\s+\d+\s+minutes)",
            re.DOTALL
        )
        
    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)

        for command_key, command_data in blocks.items():
            # Ensure we are reading the 'output' key from the command_data dictionary
            matches = self.pattern.finditer(command_data['output'])
            print('matches', matches)
            for match in matches:
                parsed_data[command_key].append(match.groupdict())
        print('parsed_data', parsed_data)   
        # Assuming merging is not required for this parser as every slot is unique
        # However, if needed, a merging logic can be implemented here
        # For the sake of this example, the merging logic is omitted
        return [val for sublist in parsed_data.values() for val in sublist]