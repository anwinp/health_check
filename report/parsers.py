
import re
from collections import defaultdict
import datetime

class CommandParserBase:
    def __init__(self):
        self.pattern = re.compile(r"^(.*?):\s*(.*)$", re.MULTILINE)
        
    def parse(self, blocks):
        raise NotImplementedError("Each parser must implement the parse method.")
    
    def merge_parsed_data(self, parsed_data):
        merged_data = []
        for key in parsed_data:
            merged_data.extend(parsed_data[key])
        return merged_data
    
    # Generic function for parsing key-value pairs with a colon
    def parse_key_value_pairs(self, text, keywords=None):
        matches = self.pattern.findall(text)
        if keywords:
            filtered_matches = [(key.strip(), value.strip()) for key, value in matches if key.strip() in keywords]
            return {key: value for key, value in filtered_matches}
        else:
            return {key.strip(): value.strip() for key, value in matches}
    
    def parse_space_separated_key_values(self, text, keywords=None):
        """
        Parses space-separated key-value pairs, filtering by a list of keywords.
        
        Args:
            text (str): The input text to parse.
            keywords (list, optional): A list of keywords to filter the keys. Defaults to None.
            
        Returns:
            dict: The parsed key-value pairs.
        """
        lines = text.strip().split('\n')
        split_index = max([line.find('  ') for line in lines if line.find('  ') != -1]) + 1

        parsed_data = {}
        for line in lines:
            if line.find('  ') != -1:  # Ensure there's a gap indicating a key-value pair
                key = line[:split_index].strip()
                value = line[split_index:].strip()
                if key and (not keywords or any(keyword.lower() in key.lower() for keyword in keywords)):
                    parsed_data[key] = value

        return parsed_data
    
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

        for command_key, command_data in blocks.items():
            result_dict = self.parse_key_value_pairs(command_data['output'], keywords=['Shelf', 'Slot', 'Type', 'Card Version', 'Software Version', 'Uptime', 'State'])
            filtered_dict = {
                'Shelf': result_dict.get('Shelf'),
                'Slot': result_dict.get('Slot'),
                'Type': result_dict.get('Type').split(',')[0].strip(),
                'Card Version': result_dict.get('Card Version'),
                'Software Version': result_dict.get('Software Version'),
                'Uptime': result_dict.get('Uptime'),
                'Additional Information': result_dict.get('Type').split(',')[1].strip(),
                'State': result_dict.get('State'),
                
            }
            parsed_data[command_key].append(filtered_dict)
        print('parsed_data', parsed_data)   

        if merge:
            return self.merge_parsed_data(parsed_data)
        else:
          return parsed_data
      
class SFPDataParser(CommandParserBase):
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
                
            result_dict = self.parse_space_separated_key_values(command_data['output'], keywords=self.keyword_mapping.keys())
            result_dict["manufacturingDateCode"] = self.format_manufacturing_date(result_dict["manufacturingDateCode"])   

            mapped_data.update({self.keyword_mapping.get(k, k): v for k, v in result_dict.items()})
            
            parsed_data[command_key].append(mapped_data)

        if merge:
            return self.merge_parsed_data(parsed_data)
        else:
            return parsed_data
