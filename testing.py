__author__ = 'Sebastian.Law'

import vendors
import main
import files

vens = vendors.load_vendors()
data = main.load_pickle(files.pickle_stub+"-2015-12-07-16-48-50.pkl")


def extract(v, i):
    return main.extract_email(data, vens, v, i)


def display(v, i, save=False):
    main.display_email(data, vens, v, i, save)


def search(date):
    main.find_mail(data, vens, date)


def run():
    t = main.extract_all(data, vens)
    main.dump_data(t, files.output_test, True)


# data = get_gmail()
# transactions = extract_all(data, vendor_list)
