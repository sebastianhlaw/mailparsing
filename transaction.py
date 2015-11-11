__author__ = 'Sebastian.Law'

import datetime


class Sale:
    def __init__(self):
        keys = (
            "vendorID",
            "execDate",
            "tickets",
            "artist",
            "venue",
            "gigTime",
            "section",
            "row",
            "seats",
            "ticketType",
            "sent",
            "paidDate",
            "postCost",
            "postRefund",
            "otherCosts",
            "unitPrice",
            "netPrice"
        )
        data = [None]*len(keys)
        self._dictionary = dict(zip(keys, data))
        self._email_time = None
        self._process_time = None

    def get_dict(self):
        return self._dictionary

    def set_data_item(self, key, data):
        if key in self._dictionary:
            self._dictionary[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def set_email_timestamp(self, timestamp):
        self._email_time = timestamp

    def set_process_time(self):
        self._process_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_headings(self):
        return ['processTime', 'emailTime'] + list(self._dictionary.keys())

    def get_data(self):
        return [self._process_time, self._email_time] + list(self._dictionary.values())
