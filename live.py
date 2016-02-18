
# import vendors
import main
import files
import datetime
import os

vendors = main.vendor_list

read_only_and_testing = True
search_string = None
if files.live_location():  # we're in the live folder
    read_only_and_testing = False
    search_string = "(UNSEEN)"
else:  # Testing mode
    search_string = "(SINCE 02-Feb-2016)"
# data = main.pull_data(vendors, read_only_and_testing, search_string)
minimal_messages = main.pull_minimal_messages("INBOX", read_only_and_testing, search_string)

today = str(datetime.date.today())
now_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
now_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
if read_only_and_testing:
    output_file = os.path.join(files.output_folder, "test-" + today + ".csv")
    pickle_file = os.path.join(files.pickle_folder, "test-" + now_filename + ".pkl")
else:
    output_file = os.path.join(files.output_folder, "sales-" + today + ".csv")
    pickle_file = os.path.join(files.pickle_folder, "sales-" + now_filename + ".pkl")
logger_file = os.path.join(files.logger_folder, "logger-"+today+".txt")

transactions = []
if minimal_messages:
    main.dump_minimal_messages(minimal_messages, pickle_file)
    print("Pickled in:", pickle_file)
    transactions = main.extract_all(minimal_messages)
    print("Transactions extracted.")
    main.dump_data(transactions, output_file, False)
    print("Data recorded in:", output_file)

log_string = now_timestamp+"\t"+str(len(minimal_messages))+" messages,\t"+str(len(transactions))+" extracted"
is_file = os.path.isfile(logger_file)
with open(logger_file, 'a') as f:
    if not is_file:
        f.write("Timestamp\t\t#\n")
    f.write(log_string+'\n')
print("Logger updated with:", log_string)
