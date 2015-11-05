__author__ = 'Sebastian.Law'

# TODO: add metadata (processing timestamp, email time?) maybe processing timestamp should be in main
# TODO: add printing out data
# TODO: date cleaning functionality

import datetime

class Sale:
    def __init__(self):
        keys = ("transactionID",
                "transactionDate",
                "ticketsSold",
                "artist",
                "venue",
                "gigTime",
                "section",
                "row",
                "seats",
                "ticketSaleType",
                "sent",
                "paidDate",
                "postageCosts",
                "postageRefunded",
                "otherCosts",
                "unitSaleValue",
                "netSaleValue")
        data = [None]*len(keys)
        self._dictionary = dict(zip(keys, data))
        self._email_timestamp = None

    def get_dict(self):
        return self._dictionary

    def set_data_item(self, key, data):
        if key in self._dictionary:
            self._dictionary[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def get_headings(self):
        return self._dictionary.keys()

    def get_data(self):
        return self._dictionary.items()



    # def clean_date(self, i):
    #     self._values[i] = datetime.datetime.strptime(self._values[i].replace("BST", "").replace("GMT", "").strip(), self._date_format)
