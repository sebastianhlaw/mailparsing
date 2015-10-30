__author__ = 'Sebastian.Law'

import os

shared_path = os.path.join(os.path.expanduser('~'), 'Dropbox', 'Shared', 'Rial Corporate Dev')
dev_path = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev')

unprocessed_path = os.path.join(shared_path, 'unprocessed emails')
processed_path = os.path.join(shared_path, 'processed emails')
output_path = os.path.join(shared_path, 'automated output')

parameters_file = os.path.join(dev_path, 'parameters', 'tables.csv')
