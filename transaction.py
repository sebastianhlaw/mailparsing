__author__ = 'Sebastian.Law'

import datetime


class Sale:
    def __init__(self):
        # These match the search input file, with simple string descriptions
        self._search_keys = ("saleID",
                             "tickets",
                             "unitPrice",
                             "netPrice",
                             "otherCosts",
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
                             "postCost",
                             "sentDate")
        self._search_dict = dict(zip(self._search_keys, [None]*len(self._search_keys)))
        self._email_time = None
        # These match Al's required outputs. Naming not so sensible, may require concatenation or manipulation from what
        # is actually extracted from the emails. The mapping from one to the other is dealt with in self._cleanup
        self._output_keys = ("processTime",
                             "extraction",
                             "Sale ID",
                             "Sale Date",
                             "Reseller",
                             "Tix Sold",
                             "Artist",
                             "Venue",
                             "Gig Date",
                             "Section",
                             "Tix Type",
                             "Sent",
                             "Paid Date",
                             "Refundable Postage Costs",
                             "Postage Refunded",
                             "Other Costs",
                             "Sale Value",
                             "Commission Rate",
                             "Paid Back from Gigtix")
        self._output_dict = dict(zip(self._output_keys, [None]*len(self._output_keys)))

    def get_dict(self):
        return self._search_dict

    def set_data_item(self, key, data):
        if key in self._search_dict:
            self._search_dict[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def set_extraction_details(self, vendor_id, extraction_version, timestamp):
        self._output_dict["processTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._output_dict["extraction"] = extraction_version
        self._email_time = timestamp
        self._output_dict["Reseller"] = vendor_id
        self._cleanup()

    def get_headings(self, debug=False):
        headings = list(self._output_keys)
        if debug:
            headings.append(["EmailTime"])
            headings.append(list(self._search_keys))
        return headings

    def get_data(self, debug=False):
        data = [self._output_dict[k] for k in self._output_keys]
        if debug:
            data.append([self._email_time])
            data.append([self._search_dict[k] for k in self._search_keys])
        return data

    def _cleanup(self):
        # "processTime" done previously
        # "extraction" done previously
        self._output_dict["Sale ID"] = self._search_dict["saleID"]
        # "Sale Date" convert from datetime to date
        self._output_dict["Sale Date"] = self._email_time.date()
        # "Reseller" done previously
        self._output_dict["Tix Sold"] = self._search_dict["tickets"]
        self._output_dict["Artist"] = self._search_dict["artist"]
        self._output_dict["Venue"] = self._search_dict["venue"]
        # "gigTime" convert to datetime from date
        time = self._search_dict["gigTime"]
        if time is not None:
            self._output_dict["Gig Date"] = str(datetime.datetime.strptime(time, "%Y-%m-%d\t%H:%M:%S").date())
        # "Section" - construct by combining "section", "row" "seat" searches
        section = self._search_dict["section"]
        if section is not None:
            if any(s in section.lower() for s in
                   ("standing", "stalls", "circle", "general", "seating", "level", "upper")):
                section = section.replace("Section", "").strip()
        row = self._search_dict["row"]
        if row is not None:
            if row == "" or row == "GA":
                row = None
            elif any(s in row.lower() for s in ("-", "not provided")):
                row = None
            else:
                row = row.replace("Row", "").strip()
        seats = self._search_dict["seats"]
        if seats is not None:
            if seats == "":
                seats = None
            elif any(s in seats.lower() for s in ("seller didn't provide seat info", "not provided")):
                seats = None
            elif seats == self._search_dict["section"]:
                seats = None
            else:
                seats = seats.replace("Seats", "").replace("Seat", "").strip()
        text = section
        if row:
            text = text + ", Row " + row
        if seats:
            text = text + ", Seat(s) " + seats
        self._output_dict["Section"] = text
        # "Tix Type" - extract the postage method from messy text
        output_key = "Tix Type"
        item = self._search_dict["ticketType"]
        if item:
            if "UPS" in item:
                self._output_dict[output_key] = "P"
            elif "Posted" in item:
                self._search_dict[output_key] = "P"
            elif "E-Ticket" in item:
                self._search_dict[output_key] = "E"
            elif "How should I send the tickets?" in item:
                self._search_dict[output_key] = "TBA"
            else:
                self._search_dict[output_key] = "[XXX] " + item
        # self._output_dict["Refundable Postage Costs"] = self._search_dict["postCost"]
        self._output_dict["Postage Refunded"] = self._search_dict["postRefund"]
        self._output_dict["Other Costs"] = self._search_dict["otherCosts"]
        self._output_dict["Sale Value"] = self._search_dict["netPrice"]