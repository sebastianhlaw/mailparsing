__author__ = 'Sebastian.Law'

import os
import processemail
import csv
import files

# get list of unprocessed email files, then process them
files = [file for file in os.listdir(files.unprocessed_path) if file.endswith('.txt')]
transactions = []
for file in files:
    print("\n" + file + "\n")
    transactions.append(processemail.processemail(files.unprocessed_path, file))

# Extract the information
with open(files.output_path + "email-log.csv", 'a', newline='') as f:
    out = csv.writer(f)
    for i, t in enumerate(transactions):
        if i == 0:
            out.writerow(t.get_headings())
        out.writerow(t.get_data())

# Move the processed emails
# for file in files:
#     os.rename(files.unprocessed_path+file, files.processed_path+file)

print('main.py complete')