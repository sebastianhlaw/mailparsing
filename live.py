__author__ = 'Sebastian.Law'

import vendors
import main
import files
import datetime

vendors = vendors.load_vendors()
data = main.pull_data(vendors, False, "(UNSEEN)", "(SINCE 02-Dec-2015)")
print("Emails pulled.")

today = str(datetime.date.today())
now_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
now_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
output_file = files.output_stub+"-"+today+".csv"
pickle_file = files.pickle_stub+"-"+now_filename+".pkl"

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

log_string = now_timestamp+"\t"+today+"\t"+str(len(transactions))+" processed."
with open(files.output_logger, 'a') as f:
    f.write(log_string+"\n")
print("Logger updated with:", log_string)