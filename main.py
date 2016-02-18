
import os
import pickle
import files
import messages
import csv
import datetime
import vendors


vendor_list = vendors.load_vendors()
error_file = os.path.join(files.logger_folder, "errors-"+str(datetime.date.today())+".txt")


def load_minimal_messages(file_name=os.path.join(files.pickle_folder, "pickle.pkl")):
    with open(file_name, 'rb') as file:
        minimal_messages = pickle.load(file)
    return minimal_messages


def dump_minimal_messages(minimal_messages, file_name=os.path.join(files.pickle_folder, "pickle.pkl")):
    with open(file_name, 'wb') as file:
        pickle.dump(minimal_messages, file)


def pull_minimal_messages(folder="INBOX", read_only=True, *args):
    connection = messages.connect()
    msgs = messages.get_messages(connection, folder, read_only, *args)
    connection.logout()
    if msgs:
        minimal_messages = [messages.MinimalMessage(m) for m in msgs]
        valid_minimal_messages = [m for m in minimal_messages if m.mail_type == "SALE"]
        print(len(minimal_messages), "messages pulled,", len(valid_minimal_messages), "valid.")
        return valid_minimal_messages
    else:
        print("0 messages to pull.")


def extract_single(minimal_message, debug=False):
    assert type(minimal_message) is messages.MinimalMessage
    transaction = None
    for v in vendor_list:
        if minimal_message.vendor == v.get_id():
            transaction = v.extract_transaction(minimal_message.content)
            transaction._email_time = minimal_message.sent_time
            break
    if debug:
        headings = transaction.get_headings(debug)
        results = transaction.get_data(debug)
        for i, h in enumerate(headings):
            buffer = " " * max(25-len(h), 0)
            print(h, buffer, "\t", results[i])
    return transaction


def extract_all(minimal_messages):
    transactions = []
    for i, m in enumerate(minimal_messages):
        try:
            transactions.append(extract_single(m))
        except Exception as e:
            with open(error_file, 'a') as f:
                f.write("\n"+str("#"*75)+"\n")
                f.write("MESSAGE NUMBER: "+str(i)+"\n")
                f.write(str("#"*25)+"\n")
                f.write(str(e)+"\n")
                f.write(str("#"*25)+"\n")
                f.write("SUBJECT:\t"+m.subject+"\n")
                f.write("SENT_TIME:\t"+str(m.sent_time)+"\n")
                f.write("VENDOR_ID:\t"+m.vendor+"\n")
                f.write("CONTENT:\n"+m.content+"\n")
            print("MESSAGE NUMBER: ", i)
            print(e)
        continue
    return transactions


# TODO: replace with MinimalMessage interface
# def find_mail_by_date(data, vendor_list, date):
#     time = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
#     for v, vendor in enumerate(vendor_list):
#         vendor_id = vendor.get_id()
#         data_subset = data[vendor_id]
#         for i, x in enumerate(data_subset):
#             if x[0] == time:
#                 print(vendor_id, v, i)


# TODO: replace with MinimalMessage interface
# def find_mail_by_id(data, vendor_list, transaction_id):
#     item = str(transaction_id)
#     for v, vendor in enumerate(vendor_list):
#         vendor_id = vendor.get_id()
#         data_subset = data[vendor_id]
#         for i, x in enumerate(data_subset):
#             if item in x[1]:
#                 print(vendor_id, v, i)

# TODO: replace with MinimalMessage interface
# def display_email(data, vendor_list, vendor_number, email_number, save_to_file=False):
#     if vendor_number >= len(vendor_list):
#         print(str(vendor_number) + " is not valid, must be < " + str(len(vendor_list)))
#         return
#     vendor = vendor_list[vendor_number]
#     vendor_id = vendor.get_id()
#     # dates = [x[0] for x in data[vendor_id]]
#     texts = [x[1] for x in data[vendor_id]]
#     if email_number >= len(texts):
#         print(str(email_number) + " is not valid, must be < " + str(len(texts)))
#         return
#     text = "\n".join(vendors.text_to_array(vendor._bespoke_replacements(texts[email_number]))
#     )
#     if save_to_file:
#         file_name = os.path.join(files.local_path, 'workings', 'debug-')+vendor_id+"("+str(vendor_number)+"-"+str(email_number)+")"
#         if save_to_file is not True:
#             file_name += "-"+str(save_to_file)
#         f = open(file_name+".txt", 'w')
#         f.write(text)
#         f.close()
#     else:
#         print(str(vendor_number)+vendor_id+"-"+str(email_number))
#         print(text)


def dump_data(transactions, file, debug=False):
    if transactions is not None:
        isfile = os.path.isfile(file)
        with open(file, 'a', newline='') as f:
            out = csv.writer(f)
            for i, t in enumerate(transactions):
                if i == 0 and not isfile:
                    out.writerow(t.get_headings(debug))
                out.writerow(t.get_data(debug))
