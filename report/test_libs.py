from .libs import process_data

def test_process_data():
    file_path = '/code/media/data/files/dgx-log_193cb2e2-6572-4d5a-a215-4b49c0732e0c.txt'
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
    