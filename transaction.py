__author__ = 'Sebastian.Law'


class Sale:
    def __init__(self):
        keys = (
            "transactionID",
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
            "netSaleValue"
        )
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

    def set_email_timestamp(self, timestamp):
        self._email_timestamp = timestamp

    def get_headings(self):
        return ['emailTimestamp'] + list(self._dictionary.keys())

    def get_data(self):
        # if self._email_timestamp is not None:
        return [self._email_timestamp] + list(self._dictionary.values())
        # else:
        #     print("email timestamp not set")
        #     return None
