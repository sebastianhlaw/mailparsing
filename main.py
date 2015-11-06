__author__ = 'Sebastian.Law'

# TODO: data dump to file
# todo: processing time in dump

import os
import files
import vendors
import pickling
import csv

debug_path_stub = os.path.join(files.local_path, 'workings', 'debug-')

vendor_list = vendors.load_vendors()

# pull the raw data
raw_data = pickling.load()  # this should be a dict
# TODO: get from gmail


# process the data into transactions
def extract_all():
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
    return transactions


def check(v, i, debug=False):
    if v >= len(vendor_list):
        print(str(v) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[v]
    vendor_id = vendor.get_id()
    items = raw_data[vendor_id]
    if i >= len(items):
        print(str(i) + " is not valid, must be < " + str(len(items)))
        return
    # text = raw_data[vendor_id][i]
    text = "\n".join(vendors.text_to_array(raw_data[vendor_id][i]))
    if debug:
        f = open(debug_path_stub+str(v)+vendor_id+"-"+str(i)+".txt", 'w')
        f.write(text)
        f.close()
    else:
        return text


def test(v, i):
    if v >= len(vendor_list):
        print(str(v) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[v]
    vendor_id = vendor.get_id()
    items = raw_data[vendor_id]
    if i >= len(items):
        print(str(i) + " is not valid, must be < " + str(len(items)))
        return
    array_item = vendors.text_to_array(items[i])  # convert the transaction string to an array
    print(vendor_id, v, "number:", i)
    return vendor.extract_transaction(array_item)
    # print(t.get_headings())
    # print(t.get_data())

# dump the transactions into the appropriate output
# with open(files.output_file, 'a', newline='') as f:
#     out = csv.writer(f)
#     for i, t in enumerate(transactions):
#         if i == 0:
#             out.writerow(t.get_headings())
#         out.writerow(t.get_data())

