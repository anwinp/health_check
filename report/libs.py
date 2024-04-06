


from .parser_factory import ParserFactory
from .log_reader import LogParser
from .report_generator import ReportGenerator
import re
import datetime
from .excel_generator import ExcelGenerator
from typing import List
from .parser_factory import ParserFactory
from .parsers import CommandParserBase
from .log_reader import LogParser
from .report_generator import ReportGenerator
from .excel_generator import ExcelGenerator
import datetime

def process_data(log_filepath: str, create_report: bool = False, create_excel: bool = True):
    # Initialize the parser factory and register command parsers
    parser_factory = ParserFactory()
    for name, ParserClass in CommandParserBase.registry.items():
        parser_factory.register_parser(name, ParserClass)
        
    log_parser = LogParser(log_filepath)
    command_keywords = list(CommandParserBase.registry.keys())
    log_parser.parse(command_keywords)   
    
    commands_data = log_parser.get_commands()

    # Step 2: Dynamically parse command outputs using registered parsers
    output = {}
    for command, blocks in commands_data.items():
        try:
            parser = parser_factory.get_parser(command)
            parsed_data = parser.parse(blocks)
            output[command] = parsed_data
        except ValueError as e:
            # import traceback
            # traceback.print_exc()
            print(e)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_filename = f"report_{timestamp}.pdf"
    excel_report_filename = f"report_{timestamp}.xlsx"

    if create_report:
        generate_report(output, report_filename)

    if create_excel:
        generate_excel_report(output, excel_report_filename)


def generate_report(output: dict, filename: str):
    report_generator = ReportGenerator(filename)
    for command, entries in output.items():
        if entries:
            heading = f"Report for {command}"
            headers = list(entries[0].keys())
            report_generator.add_table(entries, headers)
    report_generator.generate()
    print(f"Report generated at {report_generator.get_filepath()}")


def generate_excel_report(output: dict, filename: str):
    excel_generator = ExcelGenerator(filename)
    for command, entries in output.items():
        if entries:
            heading = f"Report for {command}"
            headers = list(entries[0].keys())
            excel_generator.add_table(entries, headers, sheet_name=heading)
    excel_generator.save()
    print(f"Excel generated at {excel_generator.get_filepath()}")

    

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