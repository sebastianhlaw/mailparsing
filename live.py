__author__ = 'Sebastian.Law'

import vendors
import main
import files

vendors = vendors.load_vendors()
data = main.pull_data(vendors, True, "(UNSEEN)", "(SINCE 29-Sep-2015)")
if data:
    transactions = main.extract_all(data, vendors)
    main.dump_data(transactions, files.output_file)