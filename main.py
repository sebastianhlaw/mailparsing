__author__ = 'Sebastian.Law'

import os
import processemail
import csv

# File names and locations
base_path = 'C:/Users/Sebastian.Law/Dropbox/Shared/Rial Corporate Dev/'
unprocessed_path = base_path + 'unprocessed emails/'
processed_path = base_path + 'processed emails/'
output_path = base_path + "automated output/"

# get list of unprocessed email files, then process them
files = [file for file in os.listdir(unprocessed_path) if file.endswith('.txt')]
transactions = []
for file in files:
    print("\n" + file + "\n")
    transactions.append(processemail.processemail(unprocessed_path, file))

# Extract the information
with open(output_path + "email-log.csv", 'a', newline='') as f:
    out = csv.writer(f)
    for i, t in enumerate(transactions):
        if i==0:
            out.writerow(t.get_headings())
        out.writerow(t.get_data())

# Move the processed emails
# for file in files:
#     os.rename(unprocessed_path+file, processed_path+file)

print('main.py complete')