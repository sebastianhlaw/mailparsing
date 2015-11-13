__author__ = 'Sebastian.Law'

import datetime


class Sale:
    def __init__(self):
        self._ordered_keys = ("saleID",
                              "tickets",
                              "unitPrice",
                              "netPrice",
                              "otherCosts",
                              "postCost",
                              "postRefund",
                              "ticketType",
                              "artist",
                              "venue",
                              "section",
                              "row",
                              "seats",
                              "gigTime",
                              "execDate",
                              "paidDate",
                              "sentDate")
        data = [None]*len(self._ordered_keys)
        self._dictionary = dict(zip(self._ordered_keys, data))
        self._email_time = None
        self._process_time = None
        self._vendor_id = None
        self._extraction_details = None

    def get_dict(self):
        return self._dictionary

    def set_data_item(self, key, data):
        if key in self._dictionary:
            self._dictionary[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def set_email_timestamp(self, timestamp):
        self._email_time = timestamp

    def set_extraction_details(self, vendor_id, extraction_version):
        self._process_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._vendor_id = vendor_id
        self._extraction_details = extraction_version
        self._cleanup()

    def get_headings(self):
        return ['processTime',
                'vendor',
                'extraction',
                'emailTime'] + list(self._ordered_keys)

    def get_data(self):
        results = [self._dictionary[k] for k in self._ordered_keys]
        return [self._process_time,
                self._vendor_id,
                self._extraction_details,
                self._email_time] + results

    def _cleanup(self):
        tag = "ticketType"
        item = self._dictionary[tag]
        if item:
            if "UPS" in item:
                self._dictionary[tag] = "P"
            elif "Posted" in item:
                self._dictionary[tag] = "P"
            elif "E-Ticket" in item:
                self._dictionary[tag] = "E"
            elif "How should I send the tickets?" in item:
                self._dictionary[tag] = "TBA"
            else:
                self._dictionary[tag] = "[XXX]" + item