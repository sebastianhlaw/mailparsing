
import os
import inspect


def live_location():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    return path.endswith("live")

local_path = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev')

if live_location():
    parameters_file = os.path.join(local_path, 'private', 'tables-live.csv')
else:
    parameters_file = os.path.join(local_path, 'private', 'tables-dev.csv')

# gmail_password_file = os.path.join(local_path, 'private', 'gmail_password.txt')

pickle_folder = os.path.join(local_path, 'pickles')

shared_path = os.path.join(os.path.expanduser('~'), 'Dropbox', 'Shared', 'Rial Corporate Dev')

logger_folder = os.path.join(shared_path, 'logger')
output_folder = os.path.join(shared_path, 'output')
testing_folder = os.path.join(shared_path, 'testing')
