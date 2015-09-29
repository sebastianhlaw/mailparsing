__author__ = 'Sebastian.Law'

import sys
import imaplib
import getpass
import email
import email.header
import datetime
import re

def connect():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    username = "gixtix.sales@gmail.com"
    password = getpass.getpass()
    imap.login(username, password)
    return imap

imap = connect()
# imap.list()
folders = ["SaleConfirms/GET","SaleConfirms/SEAT","SaleConfirms/STUB","SaleConfirms/VIA"]
folder = "INBOX"
typ, mailbox = imap.select(folder, True) # readonly=True

# date = (datetime.date.today() - datetime.timedelta(2)).strftime("%d-%b-%Y")
# search = '(SINCE {0})'.format(date)
search = '(UNSEEN)'
# typ, data = imap.search(None,search)
# ids = data[0].split()
# ids = [id.decode("utf-8") for id in ids]
typ, data = imap.uid("SEARCH",search)
uids = data[0].split()
uids = [uid.decode("utf-8") for uid in uids]

messages = []
for uid in uids:
    typ, data = imap.uid("FETCH", uid + ' (RFC822)')
    for part in data:
        if isinstance(part, tuple):
            messages.append(email.message_from_bytes(part[1]))
            # for header_field in [ 'subject', 'to', 'from' ]:
            #     print('%-8s: %s' % (header_field.upper(), msg[header_field]))


# fetch = uid + ' (BODY.PEEK[HEADER] FLAGS)' #'(BODY.PEEK[HEADER.FIELDS (DATE SUBJECT)])'
# typ, data = imap.uid("FETCH", fetch)

# # Print all unread messages from a certain sender of interest
# status, response = imap.search(None, '(UNSEEN)', '(FROM "%s")' % (sender_of_interest))
# unread_msg_nums = response[0].split()
# da = []
# for e_id in unread_msg_nums:
#     _, response = imap.fetch(e_id, '(UID BODY[TEXT])')
#     da.append(response[0][1])
# print da
#
# # Mark them as seen
# for e_id in unread_msg_nums:
#     imap.store(e_id, '+FLAGS', '\Seen')

# def parse_list_response(line):
#     pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
#     flags, delimiter, mailbox_name = pattern.match(line).groups()
#     mailbox_name = mailbox_name.strip('"')
#     return (flags, delimiter, mailbox_name)

# EMAIL_ACCOUNT = "sebastianhlaw@gmail.com"
# EMAIL_FOLDER = "INBOX"

# def process_mailbox(M):
#     """
#     Do something with emails messages in the folder.
#     For the sake of this example, print some headers.
#     """
#
#     rv, data = M.search(None, "ALL")
#     if rv != 'OK':
#         print("No messages found!")
#         return
#
#     for num in data[0].split():
#         rv, data = M.fetch(num, '(RFC822)')
#         if rv != 'OK':
#             print("ERROR getting message", num)
#             return
#
#         msg = email.message_from_bytes(data[0][1])
#         hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
#         subject = str(hdr)
#         print('Message %s: %s' % (num, subject))
#         print('Raw Date:', msg['Date'])
#         # Now convert to local date-time
#         date_tuple = email.utils.parsedate_tz(msg['Date'])
#         if date_tuple:
#             local_date = datetime.datetime.fromtimestamp(
#                 email.utils.mktime_tz(date_tuple))
#             print ("Local Date:", local_date.strftime("%a, %d %b %Y %H:%M:%S"))


# M = imaplib.IMAP4_SSL('imap.gmail.com')
#
# try:
#     rv, data = M.login(EMAIL_ACCOUNT, getpass.getpass())
# except imaplib.IMAP4.error:
#     print ("LOGIN FAILED!!! ")
#     sys.exit(1)
#
# print(rv, data)
#
# rv, mailboxes = M.list()
# if rv == 'OK':
#     print("Mailboxes:")
#     print(mailboxes)
#
# rv, data = M.select(EMAIL_FOLDER, True)
# if rv == 'OK':
#     print("Processing mailbox...\n")
#     process_mailbox(M)
#     M.close()
# else:
#     print("ERROR: Unable to open mailbox ", rv)
#
# M.logout()