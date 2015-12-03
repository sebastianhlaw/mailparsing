__author__ = 'Sebastian.Law'

import vendors
import main
import files
import datetime

vendors = vendors.load_vendors()
data = main.pull_data(vendors, True, "(UNSEEN)", "(SINCE 01-Dec-2015)")

today = str(datetime.date.today())
now_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
now_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
output_file = files.output_stub+"-"+today+".csv"
pickle_file = files.pickle_stub+"-"+now_filename+".pkl"

if data:
    main.dump_pickle(data, pickle_file)
    transactions = main.extract_all(data, vendors)
    main.dump_data(transactions, output_file, False)

counter = str(len(transactions))
with open(files.output_logger, 'a') as f:
    f.write(now_timestamp+"\t"+today+"\t"+counter+" processed.\n")