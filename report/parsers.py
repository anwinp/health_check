
import re
from collections import defaultdict
import datetime

class KeyValueParser:
    def parse(self, text, keywords=None):
        # Split the input text into lines
        lines = text.strip().split('\n')
        parsed_data = {}

        for line in lines:
            # Split each line at the first colon found
            parts = line.split(':', 1)
            
            # If the line contains a colon and has parts on both sides of it
            if len(parts) == 2:
                key, value = parts
                key = key.strip()
                value = value.strip()
                
                # Only add the key-value pair if there's a non-empty value
                # and if no keywords specified or the key matches one of the keywords
                if value and (not keywords or any(kw.lower() in key.lower() for kw in keywords)):
                    parsed_data[key] = value

        # Check if parsed_data is empty and print a message if so
        if not parsed_data:
            print("No key-value pairs exist in the input.")
            return None

        return parsed_data
    
    
class SpaceSeparatedKeyValueParser:
    def parse(self, text, keywords=None):
        """
        Parses space-separated key-value pairs, filtering by a list of keywords.
        
        Args:
            text (str): The input text to parse.
            keywords (list, optional): A list of keywords to filter the keys. Defaults to None.
            
        Returns:
            dict or None: The parsed key-value pairs or None if no pairs are found.
        """
        lines = text.strip().split('\n')
        parsed_data = {}

        for line in lines:
            if '  ' in line:  # Check if there is a double space, indicating a key-value pair
                key, value = line.split('  ', 1)
                key = key.strip()
                value = value.strip()
                if key and (not keywords or any(keyword.lower() in key.lower() for keyword in keywords)):
                    parsed_data[key] = value

        if not parsed_data:  # No key-value pairs found
            print("No space-separated key-value pairs exist in the input.")
            return None

        return parsed_data


class DataMerger:
    def merge(self, parsed_data):
        merged_data = []
        for key in parsed_data:
            merged_data.extend(parsed_data[key])
        return merged_data


class ParserMeta(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        elif hasattr(cls, 'command_keyword'):
            cls.registry[cls.command_keyword] = cls
        super().__init__(name, bases, attrs)
        
        
class CommandParserBase(metaclass=ParserMeta):
    def __init__(self):
        self.key_value_parser = KeyValueParser()
        self.space_separated_key_value_parser = SpaceSeparatedKeyValueParser()
        self.data_merger = DataMerger()

    def parse(self, blocks):
        raise NotImplementedError("Each parser must implement the parse method.")
    
    def return_parsed_data(self, parsed_data, merge):
        if merge:
            return self.data_merger.merge(parsed_data)
        else:
            return parsed_data


class ShowlineParser(CommandParserBase):
    command_keyword = 'showline'
    
    def parse(self, blocks, merge=True):
        # Updated to capture optional port information
        section_pattern = re.compile(
            r"shelf = (\d+),\s+slot = (\w+),\s*(?:port (\d+),)?\s*line type = (\w+)(.*?)(?=\n-{72}|\Z)",
            re.DOTALL
        )
        sub_port_pattern = re.compile(r"(\d+-\d+|\d+)\s+([A-Z\s]+)")

        parsed_data = {}

        for command_key, command_data in blocks.items():
            sections = section_pattern.findall(command_data['output'])
            parsed_data[command_key] = []

            for shelf, slot, port, line_type, statuses in sections:
                port = port or ""  # Keep port as an empty string if not present
                status_lines = statuses.strip().split('\n')
                for status_line in status_lines:
                    port_match = sub_port_pattern.match(status_line.strip())
                    if port_match:
                        sub_port_range, status = port_match.groups()
                        parsed_data[command_key].append({
                            'Shelf': shelf,
                            'Slot': slot,
                            'Port': port,  # Now including port
                            'Line Type': line_type,
                            'Sub Port Range': sub_port_range,
                            'Status': ' '.join(status.split())  # Normalize spaces
                        })
        return self.return_parsed_data(parsed_data, merge)
    
    
class SlotsParser(CommandParserBase):
    command_keyword = 'slots'
    
    def __init__(self):
        super().__init__()
        
    def parse(self, blocks, merge=True):
        """_summary_

        command_data{'command': 'slots m1', 'output': 'MXK 1419 \nType            :*MXK-MC-TOP, 14U MGMT W/ TOP\nCard Version    : 800-03576-04-B\nEEPROM Version  : 1\nSerial #        : 15691446\nCLEI Code       : No CLEI   \nCard-Profile ID : 1/m1/20001\nShelf           : 1\nSlot            : m1\nROM Version     : MXK 3.4.2.144.007\nSoftware Version: MXK 3.4.2.272\nState           : RUNNING\nMode            : FUNCTIONAL\nHeartbeat check : enabled\nHeartbeat last  : FRI MAR 22 09:19:01 2024\nHeartbeat resp  : 317647\nHeartbeat late  : 0\nHbeat seq error : 0\nHbeat longest   : 11\nFault reset     : enabled\nPower fault mon : supported\nUptime          : 3 days, 16 hours, 14 minutes\n'}
        
        Args:
            blocks (_type_): _description_
            merge (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        parsed_data = defaultdict(list)
        slots_output = blocks.pop('slots', None)
        cards_info = self.parse_cards_info(slots_output['output'])
        for command_key, command_data in blocks.items():
            result_dict = self.key_value_parser.parse(command_data['output'], keywords=['Shelf', 'Slot', 'Type', 'Card Version', 'Software Version', 'Uptime', 'State'])
            card_type = result_dict.get('Type')

            card_mapping = cards_info.get(card_type)
            filtered_dict = {
                'Component': card_mapping['component'],
                'Shelf': result_dict.get('Shelf'),
                'Slot': result_dict.get('Slot'),
                'Type': card_type.split(',')[0].strip(),
                'Card Version': result_dict.get('Card Version'),
                'Software Version': result_dict.get('Software Version'),
                'Uptime': result_dict.get('Uptime'),
                'Additional Information': card_mapping['card_key'],
                'State': result_dict.get('State'),
                'Slots Status': card_mapping['status']
                
            }
            parsed_data[command_key].append(filtered_dict)

        return self.return_parsed_data(parsed_data, merge)

    def parse_cards_info(self, text):
        lines = text.split('\n')[1:]  # Skip the first line

        # Pattern to detect category lines and card entry lines
        category_pattern = re.compile(r'^(Management Cards|Fabric Cards|Line Cards)$')
        card_entry_pattern = re.compile(r'(\w+)\s*:(.*)\((.*)\)')


        parsed_data = {}
        current_category = None

        for line in lines:
            # Check for category lines
            category_match = category_pattern.match(line.strip())
            if category_match:
                current_category = category_match.group(1)  # Capture the current category
                continue

            # Process card entry lines within the current category
            if current_category:
                card_match = card_entry_pattern.match(line.strip())
                if card_match:
                    card_key, card_detail, status = card_match.groups()
                    card_detail = card_detail.strip().split(' (')[0]  # Extract card detail, exclude status
                    # Formulate the key as 'Category CardKey': 'CardDetail'
                    parsed_data[card_detail] = {
                        'component': current_category,
                        'card_key': card_key,
                        'status': status
                    }

        return parsed_data


class SFPDataParser(CommandParserBase):
    command_keyword = 'sfp'
    
    def __init__(self):
        super().__init__()
        self.keyword_mapping = {
            "vendorName": "Vendor Name",
            "vendorPartNumber": "Vendor Part Number",
            "serialNumber": "Serial Number",
            "manufacturingDateCode": "Manufacturing Date",
            "nominalBitRate": "Nominal Bit Rate (Gbps)",
            "upperBitRateMarginPercentage": "Upper Bit Rate Margin (%)",
            "lowerBitRateMarginPercentage": "Lower Bit Rate Margin (%)"
        }
        self.interface_pattern = re.compile(r"SFP Data for interface (.+)")
        
    def extract_interface(self, command_data):
        interface_line = command_data.strip().split('\n')[0]
        interface_match = self.interface_pattern.match(interface_line)
        return interface_match.group(1) if interface_match else None

    def format_manufacturing_date(self, input_date):
        date = datetime.datetime.strptime(input_date, "%d%m%y")
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date

    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)

        for command_key, command_data in blocks.items():
            interface = self.extract_interface(command_data['output'])
            mapped_data = {}
            if interface:
                mapped_data['Interface'] = interface
                
            result_dict = self.space_separated_key_value_parser.parse(command_data['output'], keywords=self.keyword_mapping.keys())
            result_dict["manufacturingDateCode"] = self.format_manufacturing_date(result_dict["manufacturingDateCode"])   

            mapped_data.update({self.keyword_mapping.get(k, k): v for k, v in result_dict.items()})
            
            parsed_data[command_key].append(mapped_data)

        return self.return_parsed_data(parsed_data, merge)


class ShowFatalDataParser(CommandParserBase):
    command_keyword = 'showfataldata'
    
    def __init__(self):
        super().__init__()
        self.keywords = [
            "Timestamp",
            "SW version",
            "Task name",
            "Errno",
            "Fatal code",
        ]
        
    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        for command_key, command_data in blocks.items():
            result_dict = self.key_value_parser.parse(command_data['output'], keywords=self.keywords)
            if result_dict is None:
                continue
            parsed_data[command_key].append(result_dict)
        return self.return_parsed_data(parsed_data, merge)

        
class RomVersionParser(CommandParserBase):
    command_keyword = 'romversion'
    
    def __init__(self):
        super().__init__()
        
    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        for command_key, command_data in blocks.items():
            if self.command_keyword in command_key:
                # Extract card identifier (number or string) from command key
                card_identifier_match = re.search(rf'{self.command_keyword}\s+(\S+)', command_key)
                card_identifier = card_identifier_match.group(1) if card_identifier_match else "Unknown"

                # Split the command output by new lines to separate rom version and timestamp
                lines = command_data['output'].split('\n')
                if len(lines) >= 2:
                    rom_version = lines[0].strip()
                    timestamp = lines[1].strip()
                    
                    parsed_data[command_key].append({
                        'Card': card_identifier,
                        'ROM ersion': rom_version,
                        'Timestamp': timestamp
                    })
        return self.return_parsed_data(parsed_data, merge)
