__author__ = 'Sebastian.Law'


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

    def get_dict(self):
        return self._dictionary

    def set_data_item(self, key, data):
        if key in self._dictionary:
            self._dictionary[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def set_email_timestamp(self, timestamp):
        self._email_time = timestamp

    def get_headings(self):
        return ['emailTime'] + list(self._dictionary.keys())

    def get_data(self):
        # if self._email_timestamp is not None:
        return [self._email_time] + list(self._dictionary.values())
        # else:
        #     print("email timestamp not set")
        #     return None
