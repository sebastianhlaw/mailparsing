__author__ = 'Sebastian.Law'

import os
import files
import gmail
import csv
import datetime
import vendors


def pull_data(vendors, read_only=True, *search):
    # *search = "(UNSEEN)", "(SINCE 11-Nov-2015)"
    data = {}
    for v in vendors:
        key = v.get_id()
        folder = v.get_gmail_folder()
        content = gmail.get_message_contents(folder, read_only, *search)
        data.update({key: content})
    return data


def extract_all(data, vendors):
    # process the data into transactions
    transactions = []
    for vendor in vendors:  # for each vendor
        vendor_id = vendor.get_id()  # pull the id
        if vendor_id in data:  # if the vendor is present in the data pull
            pairs = data[vendor_id]  # get all transaction info for the vendor
            if pairs is not None:  # if there are transactions, loop through them
                for pair in pairs:
                    transactions.append(vendor.extract_transaction(pair))
    return transactions


def find_mail(data, vendor_list, date):
    t = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    for v, vendor in enumerate(vendor_list):
        vendor_id = vendor.get_id()
        data_subset = data[vendor_id]
        for i, x in enumerate(data_subset):
            if x[0] == t:
                print(vendor_id, v, i)
            # elif x[0].date() == t.date():
            #     print(i, x[0], "day only")


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
    text = "\n".join(vendors.text_to_array(
        vendor._bespoke_replacements(texts[email_number]),
        vendor._sale_start_tag)
    )
    if save_to_file:
        f = open(os.path.join(files.local_path, 'workings', 'debug-')+str(vendor_number)+vendor_id+"-"+str(email_number)+".txt", 'w')
        f.write(text)
        f.close()
    else:
        print(str(vendor_number)+vendor_id+"-"+str(email_number))
        print(text)


def extract_email(data, vendor_list, vendor_number, email_number):
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
    headings = t.get_headings()
    results = t.get_data()
    for email_number, h in enumerate(headings):
        print(h, "\t\t", results[email_number])
    return t


def dump_data(transactions, file):
    # file = files.output_file
    if transactions is not None:
        with open(file, 'a', newline='') as f:
            out = csv.writer(f)
            for i, t in enumerate(transactions):
                if i == 0:
                    out.writerow(t.get_headings())
                out.writerow(t.get_data())
