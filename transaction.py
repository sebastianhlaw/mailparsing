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
        self._extraction_time = None
        self._email_time = None
        self._extraction_version = None
        # These match Al's required outputs. Naming not so sensible, may require concatenation or manipulation from what
        # is actually extracted from the emails. The mapping from one to the other is dealt with in self._cleanup
        self._output_keys = ("processTime",
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
        self._venue_replacements = (("Etihad Stadium", "Etihad Stadium Manc"),
                                    ("O2 Academy Brixton", "Brixton Academy"),
                                    ("O2 Forum Kentish Town", "O2 Forum"),
                                    ("O2 Shepherds Bush Empire", "Shepherds Bush Empire"),
                                    ("SSE Arena Wembley", "Wembley Arena"),
                                    ("Forum", "O2 Forum"),
                                    ("London Royal Albert Hall", "Royal Albert Hall"))

    def get_dict(self):
        return self._search_dict

    def set_data_item(self, key, data):
        if key in self._search_dict:
            self._search_dict[key] = data
        else:
            print("key '" + key + "' is not recognised.")

    def set_extraction_details(self, vendor_id, extraction_version, timestamp):
        self._output_dict["processTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._extraction_version = extraction_version
        self._extraction_time = timestamp
        self._output_dict["Reseller"] = vendor_id
        self._cleanup()

    def get_headings(self, debug=False):
        headings = list(self._output_keys)
        if debug:
            headings.append("ExtractionTime")
            headings.append("ExtractionVersion")
            headings.append("EmailTime")
            headings.extend(list(self._search_keys))
        return headings

    def get_data(self, debug=False):
        data = [self._output_dict[k] for k in self._output_keys]
        if debug:
            data.append(self._extraction_time)
            data.append(self._extraction_version)
            data.append(self._email_time)
            data.extend([self._search_dict[k] for k in self._search_keys])
        return data

    def _cleanup(self):
        # "processTime" done previously
        # "extraction" done previously
        self._output_dict["Sale ID"] = self._search_dict["saleID"]
        # "Sale Date" convert from datetime to date
        sent_date = self._search_dict["sentDate"]
        if sent_date is not None:
            self._output_dict["Sale Date"] = str(datetime.datetime.strptime(sent_date, "%Y-%m-%d").date())
        # "Reseller" done previously
        self._output_dict["Tix Sold"] = self._search_dict["tickets"]
        self._output_dict["Artist"] = self._search_dict["artist"]
        venue = self._search_dict["venue"]
        if venue is not None:
            venue = venue.replace(" - ", " ").replace(",", "").replace("The ", "").strip()
            venue = venue.replace(" London UK", "").replace(" Wembley UK", "").replace(" Manchester UK", "")
            for x, y in self._venue_replacements:
                if venue == x:
                    venue = y
            self._output_dict["Venue"] = venue.replace("arena", "Arena")
        # "gigTime" convert to datetime from date
        time = self._search_dict["gigTime"]
        if time is not None:
            self._output_dict["Gig Date"] = str(datetime.datetime.strptime(time, "%Y-%m-%d\t%H:%M:%S").date())
        # "Section" - construct by combining "section", "row" "seat" searches
        section = self._search_dict["section"]
        if section is not None:
            if "standing" in section.lower() or "general admission" in section.lower():
                section = "Standing"
            elif any(s in section.lower() for s in ("stalls", "circle", "seating", "level", "upper")):
                section = section.replace("Section", "Block").replace("arena", "Arena").strip()
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
            text = text + " Row " + row
        if seats:
            text = text + " Seat(s) " + seats
        self._output_dict["Section"] = text
        # "Tix Type" - extract the postage method from messy text
        output_key = "Tix Type"
        item = self._search_dict["ticketType"]
        if item:
            if "UPS" in item:
                self._output_dict[output_key] = "P"
            elif "Posted" in item:
                self._output_dict[output_key] = "P"
            elif "E-Ticket" in item:
                self._output_dict[output_key] = "E"
            elif "How should I send the tickets?" in item:
                self._output_dict[output_key] = "TBA"
            else:
                self._output_dict[output_key] = item
        # self._output_dict["Refundable Postage Costs"] = self._search_dict["postCost"]
        post_refund = self._search_dict["postRefund"]
        if post_refund == 0:
            self._output_dict["Postage Refunded"] = None
        else:
            self._output_dict["Postage Refunded"] = post_refund
        self._output_dict["Other Costs"] = self._search_dict["otherCosts"]
        self._output_dict["Sale Value"] = self._search_dict["netPrice"]
        if not self._search_dict["netPrice"]:
            tickets = int(self._search_dict["tickets"])
            unit_price = float(self._search_dict["unitPrice"])
            costs = float(self._search_dict["otherCosts"]) if self._search_dict["otherCosts"] else 0.0
            self._output_dict["Sale Value"] = round(unit_price * tickets - costs, 2)
