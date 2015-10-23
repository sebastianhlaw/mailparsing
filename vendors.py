__author__ = 'Sebastian.Law'

import datetime
import re

# def extract(list, tag, offset, split_string=None, split_element=None):
#     # TODO: this function should probably be in the transaction class
#     s = None
#     for i, l in enumerate(list):
#         if l.startswith(tag):
#             if offset>0:
#                 s = list[i+offset]
#             elif offset==0:
#                 s = l.replace(tag,'')
#             break
#     if s!=None:
#         if split_string!=None and split_element!=None:
#             s = (re.split(split_string,s))[split_element]
#         s = s.replace('£','').strip()
#     return s


class Vendor:
    def __init__(self):
        self._ID = None
        self._tag = None
    def gmail_folder(self):
        return 'SaleConfirms/' + self.ID

class Stubhub(Vendor):
    def __init__(self):
        self._ID = 'STUB'
        self._tag = 'stubhub'