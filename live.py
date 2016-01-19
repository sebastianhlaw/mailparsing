__author__ = 'Sebastian.Law'

import vendors
import main
import files
import datetime
import os

vendors = vendors.load_vendors()

read_only_and_testing = True
search_string = None
if os.getcwd().endswith("live"):  # we're in the live folder
    read_only_and_testing = False
    search_string = "(UNSEEN)"
else:  # Testing mode
    search_string = "(SINCE 10-Jan-2016)"
data = main.pull_data(vendors, read_only_and_testing, search_string)

today = str(datetime.date.today())
now_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
now_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
if read_only_and_testing:
    output_file = files.output_stub+"-test-"+today+".csv"
    pickle_file = files.pickle_stub+"-test-"+now_filename+".pkl"
else:
    output_file = files.output_stub+"-"+today+".csv"
    pickle_file = files.pickle_stub+"-"+now_filename+".pkl"
logger_file = files.logger_stub+"-"+today+".txt"

has_data = False
for key, value in data.items():
    if value is not None:
        has_data = True
        break

transactions = []
if has_data:
    main.dump_pickle(data, pickle_file)
    print("Pickled in:", pickle_file)
    transactions = main.extract_all(data, vendors)
    print("Transactions extracted.")
    main.dump_data(transactions, output_file, False)
    print("Data recorded in:", output_file)

log_string = now_timestamp+"\t"+str(len(transactions))
is_file = os.path.isfile(logger_file)
with open(logger_file, 'a') as f:
    if not is_file:
        f.write("Timestamp\t\t#\n")
    f.write(log_string+'\n')
print("Logger updated with:", log_string)
