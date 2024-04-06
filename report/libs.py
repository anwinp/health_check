


from .parser_factory import ParserFactory
from .parsers import ShowlineParser, SlotsParser
from .log_reader import LogParser
from .report_generator import ReportGenerator
import re
import datetime


def process_data(log_filepath):
    # Initialize the parser factory and register command parsers
    parser_factory = ParserFactory()
    parser_factory.register_parser('showline', ShowlineParser)
    parser_factory.register_parser('slots', SlotsParser)


    # Step 1: Read and prepare data
    log_parser = LogParser(log_filepath)
    log_parser.parse(['showline', 'slots'])  # Add more keywords as needed
    commands_data = log_parser.get_commands()
    # print(commands_data)
    # Step 2: Dynamically parse command outputs using registered parsers
    output = {}
    for command, blocks in commands_data.items():
        try:
            # print(f"Command: {command}")
            # print("Output:", blocks)
            parser = parser_factory.get_parser(command)
            parsed_data = parser.parse(blocks)
            output[command] = parsed_data
            # print(f"Parsed data for {command}: {parsed_data}")
        except ValueError as e:
            print(e)
    print(output)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_filename = f"report_{timestamp}.pdf"
    report_generator = ReportGenerator(report_filename)

        # Add tables to the report with headings
    for command, entries in output.items():
        if entries:  # Only add if there's data
            report_generator.add_heading(f"Report for {command}")
            headers = list(entries[0].keys())  # Get the headers from the keys of the first entry
            report_generator.add_table(entries, headers)
    
    # Generate the report
    report_generator.generate()
    print(f"Report generated at {report_generator.get_filepath()}")
    

# def process_data(file_path):
#     commands = {}
#     current_command = None
#     command_keywords = ['showline']  # Add more command keywords to this list as needed

#     # Open the file and process the data

#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.startswith('AUTO>'):
#                 # This is a command
#                 command_line = line.strip()[5:].strip()  # Strip 'AUTO>' from the start of the line
#                 for command_name in command_keywords:
#                     if command_line.startswith(command_name + ' '):  # Check if the command line starts with the command keyword followed by a space
#                         if command_line not in commands:
#                             commands[command_line] = []
#                         current_command = {'command': command_line, 'output': ''}
#                         commands[command_line].append(current_command)
#                         break
#                 else:
#                     current_command = None
#             elif current_command is not None:
#                 # This is part of the output of the current command
#                 current_command['output'] += line
                   
#     # print('COMMANDS', commands) # Print the commands
#     format_commands(commands)
    
def format_commands(commands):
    for command_name, command_list in commands.items():
        
        print(f"Command: {command_name}")
        # for command in command_list:
        #     print(f"  - {command['command']}")
        #     print("    Output:")
        #     lines = command['output'].split('\n')
        #     for line in lines:
        #         print(f"      {li        #         print(f"      {line.strip()}")