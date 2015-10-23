__author__ = 'Sebastian.Law'

import imaplib
import getpass
import os
import email
import html2text


def connect():
    connection = imaplib.IMAP4_SSL("imap.gmail.com")
    username = "gixtix.sales@gmail.com"
    password = getpass.getpass()
    connection.login(username, password)
    return connection


def extract_content(message):
    assert type(message) == email.message.Message
    content = None
    if type(message.get_payload()) is str:
        if message.get_content_type() == 'text/plain':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
        elif message.get_content_type() == 'text/html':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
            content = html2text.html2text(content).replace("|", "").replace("---", "")
        else:
            print(os.path.basename(__file__), "ERROR")
    else:
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                content = part.get_payload(decode=True).decode(part.get_content_charset())
                break
        if content is None:  # no plain text found, may be nested in multipart
            for part in message.get_payload():
                if part.get_content_type() == 'multipart/alternative':
                    for subpart in part.get_payload():
                        if subpart.get_content_type() == 'text/plain':
                            content = subpart.get_payload(decode=True).decode(subpart.get_content_charset())
                            break
                    if content is not None:
                        break
    return content


def get_messages(connection, folder, search='(UNSEEN)'):
    # TODO: assert that the inputs are reasonable
    # imap.list()  # lists the items in the mailbox parent
    typ, mailbox = connection.select(folder, readonly=True)
    # date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    # search = '(SINCE {0})'.format(date)
    search = '(UNSEEN)'
    # typ, data = imap.search(None,search)
    # ids = data[0].split()
    # ids = [id.decode("utf-8") for id in ids]
    typ, data = connection.uid("SEARCH", search)
    uids = data[0].split()
    uids = [uid.decode("utf-8") for uid in uids]
    messages = []
    for uid in uids:
        typ, data = connection.uid("FETCH", uid + ' (RFC822)')
        for part in data:
            if isinstance(part, tuple):
                messages.append(email.message_from_bytes(part[1]))
                # for header_field in [ 'subject', 'to', 'from' ]:
                #     print('%-8s: %s' % (header_field.upper(), msg[header_field]))
    return messages


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
