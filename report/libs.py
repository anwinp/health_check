


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
import yaml
from django.conf import settings
import os
from .models import Report
from pathlib import Path
from report_data.ingestion_registry import ingestion_registry
from report_data.models import Node

COMMAND_PATTERNS_FILE = settings.BASE_DIR / 'report' / 'command_patterns.yaml'

def load_command_patterns():
    with open(COMMAND_PATTERNS_FILE, 'r') as file:
        return yaml.safe_load(file)


def get_reports_folder_path():
    media_folder = os.path.join(settings.BASE_DIR, 'media')
    data_folder = os.path.join(media_folder, 'data')
    reports_folder = os.path.join(data_folder, 'reports')
    os.makedirs(reports_folder, exist_ok=True)
    return reports_folder

def process_data(log_filepath: str, create_report: bool = False, create_excel: bool = False):
    # Initialize the parser factory and register command parsers
    print("Processing data...")
    print(f"Log file path: {log_filepath}")
    parser_factory = ParserFactory()
    for name, ParserClass in CommandParserBase.registry.items():
        parser_factory.register_parser(name, ParserClass)
    
    command_key_to_fetch_pattern = load_command_patterns()

    log_parser = LogParser(log_filepath, command_key_to_fetch_pattern)
    command_keywords = list(CommandParserBase.registry.keys())
    
    # Check if command_keywords and command_key_to_fetch_pattern keys match
    if not set(command_key_to_fetch_pattern.keys()).issubset(set(command_keywords)):
        print('command_key_to_fetch_pattern', command_key_to_fetch_pattern.keys())
        print('command_keywords', command_keywords)
        raise ValueError("Parser keys don't match Keys defined in the yaml file")
    log_parser.parse()   
    
    commands_data = log_parser.get_commands()

    file_name = Path(log_filepath).stem
    print(f"Processing data for {file_name}...")    
    ip_address = file_name.split('_')[1]
    node_instance, _ = Node.objects.get_or_create(ip_address=ip_address, name=ip_address)
    # Step 2: Dynamically parse command outputs using registered parsers
    output = {}
    for command, blocks in commands_data.items():
        try:
            parser = parser_factory.get_parser(command)
            parsed_data = parser.parse(blocks)
            output[command] = parsed_data
            ingestion_function = ingestion_registry.get_ingestion_method(command)
            if not ingestion_function:
                print(f"No ingestion method registered for command: {command}")
                continue
            ingestion_function(node_instance, parsed_data)
        except ValueError as e:
            # import traceback
            # traceback.print_exc()
            print(e)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_filename = f"report_{file_name}_{timestamp}.pdf"
    excel_report_filename = f"report_{file_name}_{timestamp}.xlsx"

    if create_report:
        generate_report(output, report_filename)

    if create_excel:
        generate_excel_report(output, excel_report_filename)


def generate_report(output: dict, filename: str):
    reports_folder = get_reports_folder_path()
    report_filepath = os.path.join(reports_folder, filename)
    report_generator = ReportGenerator(report_filepath)
    for command, entries in output.items():
        if entries:
            heading = f"Report for {command}"
            headers = list(entries[0].keys())
            report_generator.add_table(entries, headers)
    report_generator.generate()
    save_report_record(report_filepath, 'pdf')
    
    print(f"Report generated at {report_generator.get_filepath()}")


def generate_excel_report(output: dict, filename: str):
    reports_folder = get_reports_folder_path()
    excel_filepath = os.path.join(reports_folder, filename)
    excel_generator = ExcelGenerator(excel_filepath)
    for command, entries in output.items():
        if entries:
            heading = f"{command.title()}"
            headers = list(entries[0].keys())
            excel_generator.add_table(entries, headers, sheet_name=heading)
    excel_generator.save()
    save_report_record(excel_filepath, 'xlsx')

    print(f"Excel generated at {excel_generator.get_filepath()}")

    
def save_report_record(report_filepath, report_type):
    title = os.path.basename(report_filepath)
    
    # Here, just the path is being saved instead of the file itself
    report = Report(title=title, report_type=report_type, file_path=report_filepath)
    report.save()
    print(f"{report_type.upper()} report record saved with ID: {report.id}")

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