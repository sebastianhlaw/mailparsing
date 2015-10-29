__author__ = 'Sebastian.Law'

import gmail
import re


def text_to_array(text, start_from=None):
    array = re.split('\\n', text, maxsplit=0, flags=0)
    array = [l.strip() for l in array if l.strip() != '']
    if start_from is not None:
        for i, line in enumerate(array):
            if line == start_from:
                break
        if i != len(array)-1:
            array = array[i:]
    return array

connection = gmail.connect()
folders = ['INBOX', 'SaleConfirms/GET', 'SaleConfirms/SEAT', 'SaleConfirms/STUB', 'SaleConfirms/VIA']
folder = folders[0]
messages = gmail.get_messages(connection, folder)
connection.close()
contents = [gmail.extract_content(m) for m in messages]
connection.logout()



