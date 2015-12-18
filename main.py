__author__ = 'Sebastian.Law'

import os
import pickle
import files
import gmail
import csv
import datetime
import vendors


# Currently the data is pickled as a dict of the form 'SEAT': [text1, text2, ...]
def load_pickle(file_name=files.pickle_file):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    return data


def dump_pickle(data, file_name=files.pickle_file):
    with open(file_name, 'wb') as file:
        pickle.dump(data, file)


def pull_data(vendor_list, read_only=True, *search):
    # *search = "(UNSEEN)", "(SINCE 11-Nov-2015)"
    data = {}
    for v in vendor_list:
        key = v.get_id()
        folder = v.get_gmail_folder()
        content = gmail.get_message_contents(folder, read_only, *search)
        data.update({key: content})
    return data


def extract_all(data, vendor_list):
    # process the data into transactions
    transactions = []
    for vendor in vendor_list:  # for each vendor
        vendor_id = vendor.get_id()  # pull the id
        if vendor_id in data:  # if the vendor is present in the data pull
            pairs = data[vendor_id]  # get all transaction info for the vendor
            if pairs is not None:  # if there are transactions, loop through them
                for pair in pairs:
                    transactions.append(vendor.extract_transaction(pair))
    return transactions


def find_mail_by_date(data, vendor_list, date):
    time = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    for v, vendor in enumerate(vendor_list):
        vendor_id = vendor.get_id()
        data_subset = data[vendor_id]
        for i, x in enumerate(data_subset):
            if x[0] == time:
                print(vendor_id, v, i)


def find_mail_by_id(data, vendor_list, transaction_id):
    item = str(transaction_id)
    for v, vendor in enumerate(vendor_list):
        vendor_id = vendor.get_id()
        data_subset = data[vendor_id]
        for i, x in enumerate(data_subset):
            if item in x[1]:
                print(vendor_id, v, i)


def display_email(data, vendor_list, vendor_number, email_number, save_to_file=False):
    if vendor_number >= len(vendor_list):
        print(str(vendor_number) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[vendor_number]
    vendor_id = vendor.get_id()
    # dates = [x[0] for x in data[vendor_id]]
    texts = [x[1] for x in data[vendor_id]]
    if email_number >= len(texts):
        print(str(email_number) + " is not valid, must be < " + str(len(texts)))
        return
    text = "\n".join(vendors.text_to_array(vendor._bespoke_replacements(texts[email_number]))
    )
    if save_to_file:
        file_name = os.path.join(files.local_path, 'workings', 'debug-')+vendor_id+"("+str(vendor_number)+"-"+str(email_number)+")"
        if save_to_file is not True:
            file_name += "-"+str(save_to_file)
        f = open(file_name+".txt", 'w')
        f.write(text)
        f.close()
    else:
        print(str(vendor_number)+vendor_id+"-"+str(email_number))
        print(text)


def extract_email(data, vendor_list, vendor_number, email_number, debug=False):
    if vendor_number >= len(vendor_list):
        print(str(vendor_number) + " is not valid, must be < " + str(len(vendor_list)))
        return
    vendor = vendor_list[vendor_number]
    vendor_id = vendor.get_id()
    pairs = data[vendor_id]
    if email_number >= len(pairs):
        print(str(email_number) + " is not valid, must be < " + str(len(pairs)))
        return
    print(vendor_id, vendor_number, "number:", email_number)
    t = vendor.extract_transaction(pairs[email_number])
    headings = t.get_headings(debug)
    results = t.get_data(debug)
    for email_number, h in enumerate(headings):
        buffer = " " * max(25-len(h), 0)
        print(h, buffer, "\t", results[email_number])
    return t


def dump_data(transactions, file, debug=False):
    if transactions is not None:
        isfile = os.path.isfile(file)
        with open(file, 'a', newline='') as f:
            out = csv.writer(f)
            for i, t in enumerate(transactions):
                if i == 0 and not isfile:
                    out.writerow(t.get_headings(debug))
                out.writerow(t.get_data(debug))