__author__ = 'Sebastian.Law'

import os
import processemail

input_path = 'C:/Users/Sebastian.Law/Google Drive/Rial Corporate/dump/'
# filename = '2015-08-27, 160956, VIA.txt'
# root = os.path.abspath(path)

files = [file for file in os.listdir(input_path) if file.endswith('.txt')]

for file in files:
    print(file + "\n")
    t = processemail.processemail(input_path, file)

print('main.py complete')