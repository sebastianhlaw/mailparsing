__author__ = 'Sebastian.Law'

# TODO: data dump to file
# todo: processing time in dump

import os
import files
import vendors
import gmail
import pickling
import csv


# pull data from gmail
def get_gmail(vendor_list):
    data = {}
    for vendor in vendor_list:  # for each vendor
        key = vendor.get_id()
        folder = vendor.get_gmail_folder()
        message_contents = gmail.get_message_contents(folder)
        data.update({key: message_contents})
    return data


# process the data into transactions
def extract_all(data, vendors):
    transactions = []
    for vendor in vendors:  # for each vendor
        vendor_id = vendor.get_id()  # pull the id
        if data is not None:  # assuming there is some data to process
            if vendor_id in data:  # if the vendor is present in the data pull
                items = data[vendor_id]  # get all transaction info for the vendor
                if items is not None:  # if there are transactions, loop through them
                    for i, item in enumerate(items):
                        print(vendor_id, i, "====================")
                        transactions.append(vendor.extract_transaction(item))
    return transactions


debug_path_stub = os.path.join(files.local_path, 'workings', 'debug-')
vendor_list = vendors.load_vendors()
data = pickling.load()
# data = get_gmail()


def check_email(v, i, debug=False):
    if v >= len(vendor_list):
        print(str(v) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[v]
    vendor_id = vendor.get_id()
    items = data[vendor_id]
    if i >= len(items):
        print(str(i) + " is not valid, must be < " + str(len(items)))
        return
    # text = raw_data[vendor_id][i]
    text = "\n".join(vendors.text_to_array(data[vendor_id][i]))
    if debug:
        f = open(debug_path_stub+str(v)+vendor_id+"-"+str(i)+".txt", 'w')
        f.write(text)
        f.close()
    else:
        print(str(v)+vendor_id+"-"+str(i))
        print(text)


def extract_single(v, i):
    if v >= len(vendor_list):
        print(str(v) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[v]
    vendor_id = vendor.get_id()
    items = data[vendor_id]
    if i >= len(items):
        print(str(i) + " is not valid, must be < " + str(len(items)))
        return
    print(vendor_id, v, "number:", i)
    t = vendor.extract_transaction(items[i])
    headings = t.get_headings()
    results = t.get_data()
    for i, h in enumerate(headings):
        print(h, "\t\t", results[i])
    return t

# dump the transactions into the appropriate output
# with open(files.output_file, 'a', newline='') as f:
#     out = csv.writer(f)
#     for i, t in enumerate(transactions):
#         if i == 0:
#             out.writerow(t.get_headings())
#         out.writerow(t.get_data())

