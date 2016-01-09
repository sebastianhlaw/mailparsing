__author__ = 'Sebastian.Law'

import vendors
import main
import files

vens = vendors.load_vendors()
data = main.load_pickle(files.pickle_stub+"-2016-01-08-15-25-48.pkl")


def extract(v, i, debug=True):
    return main.extract_email(data, vens, v, i, debug)


def display(v, i, save=False):
    main.display_email(data, vens, v, i, save)


def search(date):  # this probably won't work now I changed date methodology
    main.find_mail(data, vens, date)


def run():
    t = main.extract_all(data, vens)
    main.dump_data(t, files.output_test, True)


# data = get_gmail()
# transactions = extract_all(data, vendor_list)
