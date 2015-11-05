__author__ = 'Sebastian.Law'

# TODO: data dump to file

import vendors
import pickling
import files
import csv


vendor_list = vendors.load_vendors()

# pull the raw data
raw_data = pickling.load()  # this should be a dict
raw_data = pickling.load()  # this should be a dict

# process the data into transactions
transactions = []
for vendor in vendor_list:  # for each vendor
    vendor_id = vendor.get_id()  # pull the id
    if raw_data is not None:  # assuming there is some data to process
        if vendor_id in raw_data:  # if the vendor is present in the data pull
            items = raw_data[vendor_id]  # get all transaction info for the vendor
            if items is not None:  # if there are transactions, loop through them
                for item in items:
                    array_item = vendors.text_to_array(item)  # convert the transaction string to an array
                    transactions.append(vendor.extract_transaction(array_item))

# dump the transactions into the appropriate output
with open(files.output_file, 'a', newline='') as f:
    out = csv.writer(f)
    for i, t in enumerate(transactions):
        if i == 0:
            out.writerow(t.get_headings())
        out.writerow(t.get_data())


# stubs = raw_data['STUB']
# text = stubs[0]
#
# array = vendors.text_to_array(text)
#
# stub = vendor_list[0]
# t = stub.extract_transaction(array)

# # get list of unprocessed email files, then process them
# files = [file for file in os.listdir(files.unprocessed_path) if file.endswith('.txt')]
# transactions = []
# for file in files:
#     print("\n" + file + "\n")
#     transactions.append(processemail.processemail(files.unprocessed_path, file))
#
# # Extract the information

#
# # Move the processed emails
# # for file in files:
# #     os.rename(files.unprocessed_path+file, files.processed_path+file)
#
# print('main.py complete')