__author__ = 'Sebastian.Law'

import gmail

connection = gmail.connect()

folders = ['SaleConfirms/GET', 'SaleConfirms/SEAT', 'SaleConfirms/STUB', 'SaleConfirms/VIA']
folder = 'INBOX'

messages = gmail.get_messages(connection, folder)
connection.close()

contents = [gmail.extract_content(m) for m in messages]


connection.logout()



