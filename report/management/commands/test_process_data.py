from report.libs import process_data
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Test the process_data function'

    def handle(self, *args, **options):
        file_path = '/Users/srikanthnadendla/PycharmProjects/visualizer/webapps/2024/Anwin_Collab/report_generator/sample_files/I3-Health-Check-04262024/log_172.16.114.24.txt' or '/code/sample_files/dgx-log.txt'
        # file_path = '/code/sample_files/dgx-log.txt'

        result = process_data(file_path)

        # # Verify the output
        # assert len(result) == 3  # Assuming there are 3 commands in the file

        # # Verify the first command
        # assert result[0]['command'] == 'command1'
        # assert result[0]['output'] == 'output1\noutput2\n'

        # # Verify the second command
        # assert result[1]['command'] == 'command2'
        # assert result[1]['output'] == 'output3\noutput4\n'

        # # Verify the third command
        # assert result[2]['command'] == 'command3'
        # assert result[2]['output'] == 'output5\noutput6\noutput7\n'

        # self.stdout.write(self.style.SUCCESS('Process data test passed successfully.'))