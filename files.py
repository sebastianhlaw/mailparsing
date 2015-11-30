__author__ = 'Sebastian.Law'

import os

local_path = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev')

parameters_file = os.path.join(local_path, 'private', 'tables.csv')
gmail_password_file = os.path.join(local_path, 'private', 'gmail_password.txt')
sebastianhlaw_password_file = os.path.join(local_path, 'private', 'sebastianhlaw_password.txt')
pickle_file = os.path.join(local_path, 'private', 'emails.pkl')

shared_path = os.path.join(os.path.expanduser('~'), 'Dropbox', 'Shared', 'Rial Corporate Dev')

output_file = os.path.join(shared_path, 'automated output', 'log.csv')
output_test = os.path.join(shared_path, 'automated output', 'test-log.csv')

# output_path = os.path.join(shared_path, 'automated output')
# unprocessed_path = os.path.join(shared_path, 'unprocessed emails')
# processed_path = os.path.join(shared_path, 'processed emails')



