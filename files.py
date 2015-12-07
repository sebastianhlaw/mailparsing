__author__ = 'Sebastian.Law'

import os

local_path = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev')

parameters_file = os.path.join(local_path, 'private', 'tables.csv')
gmail_password_file = os.path.join(local_path, 'private', 'gmail_password.txt')
sebastianhlaw_password_file = os.path.join(local_path, 'private', 'sebastianhlaw_password.txt')
pickle_file = os.path.join(local_path, 'pickles', 'emails.pkl')
pickle_stub = os.path.join(local_path, 'pickles', 'sales')

shared_path = os.path.join(os.path.expanduser('~'), 'Dropbox', 'Shared', 'Rial Corporate Dev')

logger_stub = os.path.join(shared_path, 'logger', 'logger')
output_stub = os.path.join(shared_path, 'output', 'sales')
output_test = os.path.join(shared_path, 'testing', 'sales-test.csv')
