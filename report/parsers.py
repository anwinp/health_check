
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


class ColumnBasedParser:
    def __init__(self):
        self.headers = []
        self.column_positions = []

    def detect_headers_and_data_start(self, lines):
        """Detects headers and their positions to parse columns accurately."""
        for i, line in enumerate(lines):
            if "----" in line:  # Assuming dashed lines under headers
                self.headers = re.findall(r'\S+', lines[i - 1])
                # Detect the start position of each header based on non-space characters following spaces.
                self.column_positions = [match.start() for match in re.finditer(r'\S+(?=\s|$)', lines[i - 1])]
                return i + 1  # Return the index where data starts

    def parse_line_into_columns(self, line):
        """Parses a line into data columns based on the positions of headers."""
        row_data = {}
        for header, start_pos in zip(self.headers, self.column_positions):
            end_pos = self.column_positions[self.column_positions.index(start_pos) + 1] if self.column_positions.index(start_pos) + 1 < len(self.column_positions) else None
            # Extract the substring for each column based on start and end positions.
            value = line[start_pos:end_pos].strip() if end_pos else line[start_pos:].strip()
            row_data[header] = value
        return row_data

    def parse(self, text):
        lines = text.strip().split('\n')
        data_start_line_index = self.detect_headers_and_data_start(lines)
        
        if data_start_line_index is None:
            print("Headers not detected.")
            return []

        parsed_data = []
        for line in lines[data_start_line_index:]:
            if line.strip() and not line.startswith('----'):  # Exclude dashed lines and empty lines.
                row_data = self.parse_line_into_columns(line)
                parsed_data.append(row_data)

        return parsed_data


class TextSplitter:
    @staticmethod
    def split_text_by_pattern(text, pattern):
        """
        Splits the text by a given pattern and returns a list of (header, content) tuples.
        """
        sections = re.split(pattern, text)
        headers = sections[1::2]  # Even indices after split (1, 3, 5, ...) are headers
        contents = sections[2::2]  # Odd indices after split (2, 4, 6, ...) are contents
        return list(zip(headers, contents))
    
    # @staticmethod
    # def split_text_into_sections(text):
    #     """
    #     Splits the text into sections based on dashed lines, including the section titles.

    #     Args:
    #         text (str): The input text to split.

    #     Returns:
    #         list: A list of sections, each represented as a string including its title.
    #     """
    #     # This pattern looks for any text followed by a line of dashes and captures everything
    #     # until the next line of dashes or the end of the text. It also captures the line immediately
    #     # preceding the dashes, assuming it's the title.
    #     pattern = r'(.*\n)?-+\n(.*?)(?=-+\n|$)'
        
    #     sections = []
    #     for match in re.finditer(pattern, text, re.DOTALL):
    #         section_title, section_content = match.groups()
    #         if section_title:
    #             section = f"{section_title}{section_content}".strip()
    #         else:
    #             section = section_content.strip()
    #         sections.append(section)
        
    #     return sections
    
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
        self.column_based_key_value_parser = ColumnBasedParser()
        self.data_merger = DataMerger()

    def parse(self, blocks):
        raise NotImplementedError("Each parser must implement the parse method.")
    
    def return_parsed_data(self, parsed_data, merge):
        if merge:
            return self.data_merger.merge(parsed_data)
        else:
            return parsed_data


class ShowlineParser(CommandParserBase):
    command_keyword = 'Line-Stats'
    
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
    command_keyword = 'Slots - Status'
    
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
            result_dict = self.key_value_parser.parse(command_data['output'], keywords=['Shelf', 'Slot', 'Type', 'Card Version', 'Software Version', 'Uptime', 'State', 'ROM Version', 'Mode', 'Serial #'])
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
                'Mode': result_dict.get('Mode'),
                'ROM Version': result_dict.get('ROM Version'),
                'Serial Number': result_dict.get('Serial #'),
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
    command_keyword = 'HW Inventory - Sfp'
    
    def __init__(self):
        super().__init__()
        self.keyword_mapping = {
            "vendorName": "Vendor Name",
            "vendorOui": "Vendor OUI",
            "vendorPartNumber": "Vendor Part Number",
            "vendorRevisionLevel": "Vendor Revision Level",
            "serialNumber": "Serial Number",
            "manufacturingDateCode": "Manufacturing Date",
            "connectorType": "Connector Type",
            "transceiverType": "Transceiver Type",
            "nominalBitRate": "Nominal Bit Rate (Gbps)",
            "nineTo125mmFiberLinkLengthKm": "9/125mm Fiber Link Length (km)",
            "nineTo125mmFiberLinkLength100m": "9/125mm Fiber Link Length (100m)",
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
    command_keyword = 'Alarms - Fatal Logs'
    
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
        splitter = TextSplitter()

        fatal_record_pattern = re.compile(r'(Fatal record#\s*\d+)')

        for command_key, command_data in blocks.items():
            # Use the splitter function to divide the text into sections by "Fatal record#"
            records = splitter.split_text_by_pattern(command_data['output'], fatal_record_pattern)

            for header, content in records:
                # Extract the record number from the header
                record_number_match = re.search(r'Fatal record#\s*(\d+)', header)
                record_number = record_number_match.group(1) if record_number_match else "Unknown"

                # Parse the content of each record
                result_dict = self.key_value_parser.parse(content, keywords=self.keywords)
                if result_dict:
                    result_dict["Card Number"] = record_number
                    parsed_data[command_key].append(result_dict)

        return self.return_parsed_data(parsed_data, merge)

        
class RomVersionParser(CommandParserBase):
    command_keyword = 'HW Inventory - Card ROM Version'
    
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


class AlarmParser(CommandParserBase):
    command_keyword = 'Alarms'
    
    def __init__(self):
        super().__init__()
        
    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        for command_key, command_data in blocks.items():
            result_dict = self.column_based_key_value_parser.parse(command_data['output'])
            parsed_data[command_key].extend(result_dict)
        return self.return_parsed_data(parsed_data, merge)
    
    

# class ShelfCtrlParser(CommandParserBase):
    # command_keyword = 'shelfctrl monitor'
    
    # def __init__(self):
    #     super().__init__()
        
    # def parse_section(self, section_name, section_content):
    #     """
    #     Parse individual section of the shelfctrl monitor output.
    #     """
    #     parsed_section_data = []

    #     # Handle different sections with custom logic
    #     if "Chassis Temperatures" in section_name or "Fan Power Supplies & Alarm" in section_name:
    #         lines = section_content.split("\n")
    #         for line in lines:
    #             if ":" in line:  # Key-Value pair
    #                 key, value = [part.strip() for part in line.split(":", 1)]
    #                 parsed_section_data.append({"Component": key, "Status": value})
    #             elif line.strip() and not line.startswith("----"):  # Other entries
    #                 components = re.split(r'\s{2,}', line.strip())  # Split on two or more spaces
    #                 if len(components) == 2:
    #                     parsed_section_data.append({"Component": components[0], "Status": components[1]})
    #     elif "Device" in section_name:
    #         # Similar logic to above, adjusted for "Device" section specifics
    #         lines = section_content.split("\n")
    #         for line in lines:
    #             if line.strip() and not line.startswith("----"):
    #                 key, value = [part.strip() for part in line.split("\t", 1)]
    #                 parsed_section_data.append({"Component": key, "Status": value})
    #     # Extend this if-elif block for other specific sections as needed

    #     return parsed_section_data

    # def parse(self, blocks, merge=True):
    #     parsed_data = defaultdict(list)
    #     for command_key, command_data in blocks.items():
    #         sections = TextSplitter.split_text_into_sections(command_data['output'])
    #         for section_name, section_content in sections:
    #             section_parsed_data = self.parse_section(section_name, section_content)
    #             if section_parsed_data:
    #                 parsed_data[command_key].extend(section_parsed_data)
        
    #     return self.return_parsed_data(parsed_data, merge)
    

class EEShowBackPlaneParser(CommandParserBase):
    command_keyword = 'HW Inventory Backplane'
    
    def __init__(self):
        super().__init__()
        
    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        for command_key, command_data in blocks.items():
            result_dict = self.key_value_parser.parse(command_data['output'])
            parsed_data[command_key].append(result_dict)
        return self.return_parsed_data(parsed_data, merge)
    

class GponOnuStatusParser(CommandParserBase):
    command_keyword = 'GPON-ONU-Stats'
    
    def __init__(self):
        super().__init__()
        
    def extract_slot(self, command):
        """
        Extracts the slot information from a command string.

        :param command: A string containing the command.
        :return: A string formatted as 'x-y' where x is the slot after 'rcom' and y is the slot after 'showall'.
        """
        # Regular expression to find numbers after 'rcom' and 'showall'
        match = re.search(r'rcom (\d+) gpononuponstat showall (\d+)', command)
        if match:
            slot_rcom = match.group(1)
            slot_showall = match.group(2)
            return f"{slot_rcom}-{slot_showall}"
        return "No slot info found"

    def parse_gpon_data(self, output, slot, keywords):
        """
        Parses GPON ONU status output into a list of dictionaries, each containing metrics for a single subport.

        :param output: Multi-line string containing the command output.
        :param keywords: List of keywords to include in the output.
        :return: List of dictionaries where each dictionary contains data for a single subport.
        """
        subport_data = defaultdict(dict)
        keywords_regex = '|'.join(re.escape(keyword) for keyword in keywords)  # Prepare regex pattern for keywords
        pattern = rf'ONU\(\d+\) ({keywords_regex}):\s+(\d+)'

        lines = output.split('\n')
        for line in lines:
            match = re.search(pattern, line)
            if match:
                metric = match.group(1).strip()
                value = int(match.group(2).strip())
                subport = line.split()[0]  # Extract 'ONU(1)' or similar

                if subport not in subport_data:
                    subport_data[subport]['Slot'] = slot
                    subport_data[subport]['Sub Port'] = subport
                    
                subport_data[subport][metric] = value
                

        # Convert the dictionary to a list of dictionaries
        return list(subport_data.values())

    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        keywords = [
            "Upstream Bip UNits", "FEC Corrected Bytes", "FEC Corrected codewords",
            "FEC Uncorrected codewords", "Total received codewords", "received bytes",
            "received packets", "transmitted bytes", "transmitted packets",
            "Unreceived bursts", "BIP Error", "Remote BIP Error", "Drift of Window Indications"
        ]
        for command_key, command_data in blocks.items():
            slot = self.extract_slot(command_key)
            result = self.parse_gpon_data(command_data['output'], slot, keywords)
            # result_dict = self.column_based_key_value_parser.parse(command_data['output'])
            parsed_data[command_key].extend(result)
        return self.return_parsed_data(parsed_data, merge)
    
class CardStatsParser(CommandParserBase):
    command_keyword = 'Card Stats'
    
    def __init__(self):
        super().__init__()
    
    def parse_card_stats(self, data):
        """
        Parses a block of system status data into a list of dictionaries with formatted values.
        Uses detailed regular expressions to accurately extract each field based on expected patterns.
        :param data: Multi-line string containing the raw data.
        :return: List of dictionaries where each dictionary represents the status of one slot.
        """
        # Split the data into lines
        lines = data.strip().split('\n')
        
        # Define a regex that matches the detailed structure of each line
        line_regex = re.compile(
            r'(\w+\*?)\s+'  # Slot, possibly with an asterisk
            r'(\d+)\s+'  # CPU Idle (%)
            r'(\d+)\s+'  # CPU Usage (%)
            r'(\d+)\s+'  # CPU high (not used)
            r'(\d+)\s+'  # services (not used)
            r'(\d+)\s+'  # framework (not used)
            r'(\d+)\s+'  # low (not used)
            r'(\d+\.\d+)\s+'  # Memory Utilization (%)
            r'(\d+)\s+'  # Card Memory Used (KB)
            r'(\d+)\s+'  # Card Memory Peak (KB)
            r'(\d+)\s+'  # Card Memory Available (KB)
            r'(\d+ - OK)\s+'  # Status
            r'(\d{1,2}:\d{2}:\d{2}:\d{2})\s+'  # Uptime
            r'(.+)$'  # Software Version
        )
        
        parsed_data = []
        for line in lines[2:]:  # skip the header lines
            match = line_regex.match(line.strip())
            if match:
                # Extract all matched groups
                groups = match.groups()
                slot_data = {
                    "Slot": groups[0],
                    "CPU Idle (%)": int(groups[1]),
                    "CPU Usage (%)": int(groups[2]),
                    "Memory Utilization (%)": float(groups[7]),
                    "Card Memory Total (KB)": format(int(groups[8]), ','),
                    "Card Memory Peak (KB)": format(int(groups[9]), ','),
                    "Card Memory Available (KB)": format(int(groups[10]), ','),
                    "Status": groups[11],
                    "Uptime": groups[12],
                    "Software Version": groups[13]
                }
                parsed_data.append(slot_data)
        
        return parsed_data

    def parse(self, blocks, merge=True):
        parsed_data = defaultdict(list)
        for command_key, command_data in blocks.items():
            result_dict = self.parse_card_stats(command_data['output'])
            parsed_data[command_key].extend(result_dict)
        return self.return_parsed_data(parsed_data, merge)