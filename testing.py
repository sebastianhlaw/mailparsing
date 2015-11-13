__author__ = 'Sebastian.Law'

import vendors
import pickling
import main
import files

vens = vendors.load_vendors()
data = pickling.load()


def extract(v, i):
    return main.extract_email(data, vens, v, i)


def display(v, i, save=False):
    main.display_email(data, vens, v, i, save)


def search(date):
    main.find_mail(data, vens, date)


def run():
    t = main.extract_all(data, vens)
    main.dump_data(t, files.output_test)


# data = get_gmail()
# transactions = extract_all(data, vendor_list)