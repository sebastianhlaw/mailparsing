__author__ = 'Sebastian.Law'

import os

private_path = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev', 'private')

parameters_file = os.path.join(private_path, 'tables.csv')
password_file = os.path.join(private_path, 'password.txt')
pickle_file = os.path.join(private_path, 'emails.pkl')

shared_path = os.path.join(os.path.expanduser('~'), 'Dropbox', 'Shared', 'Rial Corporate Dev')

output_file = os.path.join(shared_path, 'automated output', 'log.csv')

# output_path = os.path.join(shared_path, 'automated output')
# unprocessed_path = os.path.join(shared_path, 'unprocessed emails')
# processed_path = os.path.join(shared_path, 'processed emails')



